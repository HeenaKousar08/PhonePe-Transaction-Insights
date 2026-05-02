import streamlit as st
import pandas as pd
import plotly.express as px
import json, os, io
from sqlalchemy import create_engine
from urllib.parse import quote_plus
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest

# ==========================================
# 1. DATABASE & ENGINE SECTION
# ==========================================
@st.cache_resource
def get_engine():
    username = "heena"
    password = quote_plus("Heena@08")
    return create_engine(f"mysql+pymysql://{username}:{password}@127.0.0.1:3306/phonepe")

engine = get_engine()

@st.cache_data
def load_data():
    df = pd.read_sql("SELECT * FROM aggregated_transaction", engine)
    df.columns = df.columns.str.strip().str.lower()
    # Map DB names to internal logic
    if 'category' in df.columns: df['transaction_type'] = df['category']
    if 'count' in df.columns: df['transaction_count'] = df['count']
    if 'amount' in df.columns: df['amount'] = df['amount']
    df['state'] = df['state'].str.lower()
    return df

df = load_data()

# ==========================================
# 2. UI CONFIG & SIDEBAR
# ==========================================
st.set_page_config(page_title="PhonePe Intelligence Pro", page_icon="📱", layout="wide")

PRIMARY_COLOR = "#5F259F" 
SECONDARY_COLOR = "#F4F7F9" 

st.markdown(f"""
<style>
[data-testid="stAppViewContainer"] {{background-color: {SECONDARY_COLOR};}}
.stMetric {{background: white; padding: 20px; border-radius: 10px; border: 1px solid #E0E0E0;}}
.insight-box {{
    background-color: #ffffff; padding: 20px; border-radius: 8px;
    border-left: 5px solid {PRIMARY_COLOR}; margin: 15px 0;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.05);
}}
.insight-title {{color: {PRIMARY_COLOR}; font-weight: bold; font-size: 16px; margin-bottom: 5px;}}
h1, h2, h3 {{color: {PRIMARY_COLOR};}}
</style>
""", unsafe_allow_html=True)

st.sidebar.title("📊 Control Panel")
state_list = sorted(df['state'].unique())
selected_state = st.sidebar.selectbox("State Selection", state_list)
selected_year = st.sidebar.selectbox("Fiscal Year", sorted(df['year'].unique()))

st.sidebar.markdown("---")
target_metric = st.sidebar.radio("Metric Filter", ["amount", "transaction_count"], 
                                format_func=lambda x: "Value (₹)" if x == "amount" else "Count")

# ==========================================
# 3. GLOBAL CHART HELPER
# ==========================================
def render_pro_chart(data, x, y, title, c_type, color=None):
    if c_type == "Line":
        return px.line(data, x=x, y=y, color=color, markers=True, title=title, template="plotly_white", color_discrete_sequence=[PRIMARY_COLOR])
    elif c_type == "Bar":
        return px.bar(data, x=x, y=y, color=color, title=title, template="plotly_white", color_discrete_sequence=[PRIMARY_COLOR])
    elif c_type == "Area":
        return px.area(data, x=x, y=y, color=color, title=title, template="plotly_white", color_discrete_sequence=[PRIMARY_COLOR])
    else:
        return px.scatter(data, x=x, y=y, color=color, title=title, template="plotly_white", color_discrete_sequence=[PRIMARY_COLOR])

# ==========================================
# 4. HEADER
# ==========================================
# ==========================================
# 4. HEADER
# ==========================================
st.markdown("""
<div style='text-align:center'>
<img src="https://download.logo.wine/logo/PhonePe/PhonePe-Logo.wine.png" width="70">
<h1>PhonePe AI-Powered Transaction Insights</h1>
</div>
<hr>
""", unsafe_allow_html=True)

# ==========================================
# 5. TABS
# ==========================================
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📉 Dashboard", "🌍 India Map", "🧠 AI Analytics", "🔮 Predictions", "📂 SQL Intelligence"])

# ---- TAB 1: DASHBOARD ----
with tab1:
    f_df = df[(df['state'] == selected_state) & (df['year'] == selected_year)]
    if not f_df.empty:
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Transaction Value", f"₹ {f_df['amount'].sum():,.0f}")
        c2.metric("Total Volume", f"{f_df['transaction_count'].sum():,.0f}")
        c3.metric("Avg. Ticket Size", f"₹ {f_df['amount'].mean():,.0f}")

    col_chart, col_ctrl = st.columns([4, 1])
    with col_ctrl: chart_choice = st.selectbox("Visual Mode", ["Area", "Line", "Bar"], key="t1")
    with col_chart:
        year_data = df[df['state'] == selected_state].groupby('year')[target_metric].sum().reset_index()
        st.plotly_chart(render_pro_chart(year_data, 'year', target_metric, f"Growth Path: {selected_state.title()}", chart_choice), use_container_width=True)
    
    st.markdown(f"""<div class="insight-box"><div class="insight-title">Strategic Summary</div>
    The spending behavior in {selected_state.title()} for {selected_year} is driven by an average ticket size of ₹{f_df['amount'].mean():,.2f}.</div>""", unsafe_allow_html=True)

# ---- TAB 2: INDIA MAP (PRESERVED) ----
with tab2:
    st.markdown("## 🌍 India Map")
    df['state_clean'] = df['state'].str.replace("-", " ", regex=False).str.replace("&", "and", regex=False).str.strip().str.title()
    state_mapping = {"Andaman And Nicobar Islands": "Andaman and Nicobar Islands", "Nct Of Delhi": "Delhi", "Jammu And Kashmir": "Jammu & Kashmir"}
    df['state_clean'] = df['state_clean'].replace(state_mapping)

    geo_path = os.path.join(os.path.dirname(__file__), "india_states.geojson")
    try:
        with open(geo_path) as f:
            geojson = json.load(f)
        KEY = next((k for k in ['ST_NM', 'state', 'NAME_1', 'name'] if k in geojson['features'][0]['properties']), None)
        if KEY:
            map_data = df.groupby('state_clean')[target_metric].sum().reset_index()
            fig_map = px.choropleth(map_data, geojson=geojson, featureidkey=f"properties.{KEY}", locations="state_clean", color=target_metric, color_continuous_scale="Turbo")
            fig_map.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig_map, use_container_width=True)
            
            # --- INSIGHTS FOR TAB 2 ---
            top_map_state = map_data.sort_values(target_metric, ascending=False).iloc[0]
            st.markdown(f"""
            <div class="insight-box">
            <div class="insight-title">🌍 Geographic Intelligence</div>
            <li><b>National Leader:</b> <b>{top_map_state['state_clean']}</b> dominates the digital landscape with the highest overall {target_metric.replace('_',' ')}.</li>
            <li><b>Regional Disparity:</b> The contrast in the heatmap highlights the digital divide, showing where infrastructure expansion is most needed versus where the market is saturated.</li>
            </div>
            """, unsafe_allow_html=True)
    except:
        st.error("GeoJSON missing. Geographic analysis disabled.")

# ---- TAB 3: AI ANALYTICS (ADVANCED CLUSTERING) ----
with tab3:
    st.markdown("### 🧠 Market Segmentation & Behavior")
    t3_choice = st.selectbox("Clustering View", ["Scatter", "Bar"], key="t3")
    
    # Advanced Multi-Feature Clustering
    cluster_df = df.groupby('state').agg({'amount': 'sum', 'transaction_count': 'sum'}).reset_index()
    X = StandardScaler().fit_transform(cluster_df[['amount', 'transaction_count']])
    cluster_df['cluster'] = KMeans(n_clusters=3, random_state=42, n_init=10).fit_predict(X)
    
    st.plotly_chart(render_pro_chart(cluster_df, 'transaction_count', 'amount', "Market Tier Analysis", t3_choice, color='cluster'), use_container_width=True)
    st.markdown("""<div class="insight-box"><div class="insight-title">AI Interpretation</div>
    The algorithm has partitioned states into 3 behavioral clusters. High-volume, high-value states appear in the upper right, representing mature digital economies.</div>""", unsafe_allow_html=True)
# ---- TAB 4: PREDICTIONS ----
with tab4:
    st.markdown("### 🔮 Revenue Forecasting")
    t4_choice = st.selectbox("Projection Style", ["Line", "Area"], key="t4")
    all_y = df.groupby('year')[target_metric].sum().reset_index()
    
    if len(all_y) > 2:
        model = make_pipeline(PolynomialFeatures(2), LinearRegression()).fit(all_y[['year']], all_y[target_metric])
        future = pd.DataFrame({'year': [2025, 2026, 2027]})
        future[target_metric] = model.predict(future)
        combined = pd.concat([all_y.assign(Status='Historical'), future.assign(Status='Forecast')])
        st.plotly_chart(render_pro_chart(combined, 'year', target_metric, "Forward Outlook to 2027", t4_choice, color='Status'), use_container_width=True)
        st.markdown(f"""<div class="insight-box"><div class="insight-title">Forecast Insight</div>
        The trend suggests a <b>{'positive' if future.iloc[-1][target_metric] > all_y.iloc[-1][target_metric] else 'corrective'}</b> trajectory for the upcoming years.</div>""", unsafe_allow_html=True)
# ---- TAB 5: SQL INTELLIGENCE (PROFESSIONAL TABLES & CHARTS) ----
with tab5:
    st.markdown("### 📂 Global SQL Aggregations")
    t5_choice = st.selectbox("Aggregation Visual", ["Bar", "Line"], key="t5")

    # Clean SQL Queries matching DESCRIBE output
    top_states = pd.read_sql("SELECT state, SUM(amount) as total FROM aggregated_transaction GROUP BY state ORDER BY total DESC LIMIT 10", engine)
    cat_perf = pd.read_sql("SELECT category, SUM(amount) as total FROM aggregated_transaction GROUP BY category ORDER BY total DESC", engine)

    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown("**Top Performers (State)**")
        st.dataframe(top_states, use_container_width=True, hide_index=True)
        st.plotly_chart(render_pro_chart(top_states, 'state', 'total', "", t5_choice), use_container_width=True)
    with col_r:
        st.markdown("**Transaction Category Split**")
        st.dataframe(cat_perf, use_container_width=True, hide_index=True)
        st.plotly_chart(render_pro_chart(cat_perf, 'category', 'total', "", t5_choice), use_container_width=True)

    st.markdown(f"""<div class="insight-box"><div class="insight-title">Database Insights</div>
    The highest volume category is <b>{cat_perf.iloc[0]['category']}</b>, while <b>{top_states.iloc[0]['state'].title()}</b> leads in national revenue contribution.</div>""", unsafe_allow_html=True)

# ==========================================
# 6. FOOTER (FIXED NameError: selected_year)
# ==========================================
st.sidebar.markdown("---")
st.sidebar.write("📤 **Data Export**")
csv = df.to_csv(index=False).encode('utf-8')
# FIXED: Changed {year} to {selected_year}
st.sidebar.download_button("📩 Download Professional Report", data=csv, file_name=f"PhonePe_Insights_{selected_year}.csv", mime='text/csv')
st.sidebar.caption("Data Source: Aggregated PhonePe Transactions (MySQL)")
st.markdown("<hr><center>Developed by Heena Kousar | Professional Edition v4.5</center>", unsafe_allow_html=True)
