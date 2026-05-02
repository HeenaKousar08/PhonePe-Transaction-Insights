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
def load_base_data():
    df = pd.read_sql("SELECT * FROM aggregated_transaction", engine)
    df.columns = df.columns.str.strip().str.lower()
    # Map DB names to internal logic
    if 'category' in df.columns: df['transaction_type'] = df['category']
    if 'count' in df.columns: df['transaction_count'] = df['count']
    df['state'] = df['state'].str.lower()
    return df

@st.cache_data
def load_district_data(state_name):
    query = f"SELECT * FROM map_transaction WHERE state = '{state_name}'"
    df = pd.read_sql(query, engine)
    df.columns = df.columns.str.strip().str.lower()
    return df

@st.cache_data
def load_pincode_data(state_name):
    query = f"SELECT * FROM top_transaction_pincode WHERE state = '{state_name}'"
    df = pd.read_sql(query, engine)
    df.columns = df.columns.str.strip().str.lower()
    return df

df = load_base_data()

# ==========================================
# 2. UI CONFIG & SIDEBAR
# ==========================================
st.set_page_config(page_title="PhonePe Intelligence Pro", page_icon="📱", layout="wide")

PRIMARY_COLOR = "#5F259F" 
SECONDARY_COLOR = "#F4F7F9" 

# --- UPDATED CSS SECTION ---
st.markdown(f"""
<style>
/* Main Background */
[data-testid="stAppViewContainer"] {{
    background-color: {SECONDARY_COLOR};
}}

/* SIDEBAR STYLING */
[data-testid="stSidebar"] {{
    background-color: {PRIMARY_COLOR};
}}

/* Sidebar Text and Labels to White */
[data-testid="stSidebar"] .stMarkdown, 
[data-testid="stSidebar"] p, 
[data-testid="stSidebar"] h1, 
[data-testid="stSidebar"] h2, 
[data-testid="stSidebar"] h3, 
[data-testid="stSidebar"] label {{
    color: white !important;
}}

/* FIX: DOWNLOAD BUTTON STYLING */
div.stDownloadButton > button {{
    background-color: white !important;
    color: black !important; /* Force text color to black */
    border: 2px solid #E0E0E0;
    border-radius: 8px;
    padding: 0.5rem 1rem;
    width: 100%;
}}

/* Ensure the text inside the button is visible and black */
div.stDownloadButton > button p {{
    color: black !important;
    font-weight: normal !important;
}}

/* Hover effect for the button */
div.stDownloadButton > button:hover {{
    background-color: #f0f0f0 !important;
    border-color: {PRIMARY_COLOR};
}}

/* Metric Card Styling */
.stMetric {{
    background: white; 
    padding: 20px; 
    border-radius: 10px; 
    border: 1px solid #E0E0E0;
}}

.insight-box {{
    background-color: #ffffff; padding: 20px; border-radius: 8px;
    border-left: 5px solid {PRIMARY_COLOR}; margin: 15px 0;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.05);
}}

h1, h2, h3 {{color: {PRIMARY_COLOR};}}
</style>
""", unsafe_allow_html=True)

# --- UPDATED HEADER (LOGO TO MEDIUM) ---
st.markdown("""
<div style='text-align:center'>
<img src="https://download.logo.wine/logo/PhonePe/PhonePe-Logo.wine.png" width="180">
<h1 style='margin-top: -20px;'>PhonePe AI-Powered Transaction Insights</h1>
</div>
<hr>
""", unsafe_allow_html=True)
# HIERARCHICAL SELECTION
state_list = sorted(df['state'].unique())
selected_state = st.sidebar.selectbox("1. State Selection", state_list)

# Load context-specific data
dist_df = load_district_data(selected_state)
pin_df = load_pincode_data(selected_state)

district_list = sorted(dist_df['district'].unique()) if not dist_df.empty else []
selected_district = st.sidebar.selectbox("2. District (Deep Dive)", ["All Districts"] + district_list)

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

def format_intl_amount(number):
    """Converts raw numbers to international Billion/Million/K format"""
    if number >= 1_000_000_000:
        return f"₹ {number / 1_000_000_000:.2f} Billion"
    elif number >= 1_000_000:
        return f"₹ {number / 1_000_000:.2f} Million"
    elif number >= 1_000:
        return f"₹ {number / 1_000:.1f} K"
    else:
        return f"₹ {number:,.2f}"

def format_intl_qty(number):
    """Formats volumes into M/K suffixes"""
    if number >= 1_000_000:
        return f"{number / 1_000_000:.2f} M"
    elif number >= 1_000:
        return f"{number / 1_000:.1f} K"
    else:
        return f"{number:,}"

# ==========================================
# 5. TABS
# ==========================================
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📉 Dashboard", "🌍 India Map", "🧠 AI Analytics", "🔮 Predictions", "📂 SQL Intelligence"])
# ---- TAB 1: DASHBOARD (STATE -> DISTRICT DRILL-DOWN) ----
with tab1:
    # 1. Logic for Hierarchical View
    if selected_district == "All Districts":
        f_df = df[(df['state'] == selected_state) & (df['year'] == selected_year)]
        header_text = f"Overview: {selected_state.title()}"
    else:
        # Filtering district data loaded from map_transaction
        f_df = dist_df[(dist_df['district'] == selected_district) & (dist_df['year'] == selected_year)]
        header_text = f"Deep Dive: {selected_district.title()}"

    st.subheader(header_text)
    
    if not f_df.empty:
        # 2. Aggregations
        total_amt = f_df['amount'].sum()
        cnt_col = 'count' if 'count' in f_df.columns else 'transaction_count'
        total_vol = f_df[cnt_col].sum()
        avg_ticket = total_amt / total_vol if total_vol > 0 else 0
        
        # 3. Metrics with International Formats
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Total Transaction Value", format_intl_amount(total_amt))
        with c2:
            st.metric("Total Volume", format_intl_qty(total_vol))
        with c3:
            st.metric("Avg. Ticket Size", f"₹ {avg_ticket:,.2f}")

    # 4. Charts and Pincode Breakdown
    col_chart, col_pincode = st.columns([3, 2])
    
    with col_chart:
        chart_choice = st.selectbox("Visual Mode", ["Area", "Line", "Bar"], key="t1_viz")
        # Visualizing growth for the selected state over time
        year_data = df[df['state'] == selected_state].groupby('year')[target_metric].sum().reset_index()
        st.plotly_chart(render_pro_chart(year_data, 'year', target_metric, 
                                        f"Growth Timeline: {selected_state.title()}", chart_choice), 
                        use_container_width=True)

    with col_pincode:
        st.markdown("### 📍 Pincode Micro-Analysis")
        if not pin_df.empty:
            # Filter pincode data for selected year and format for international reading
            top_pins = pin_df[pin_df['year'] == selected_year].sort_values(by='amount', ascending=False).head(10).copy()
            top_pins['amount'] = top_pins['amount'].apply(format_intl_amount)
            top_pins['count'] = top_pins['count'].apply(format_intl_qty)
            
            st.dataframe(top_pins[['pincode', 'count', 'amount']], 
                         use_container_width=True, hide_index=True)
        else:
            st.info("Pincode table not loaded. Run fix_db.py to enable.")


# ---- TAB 2: INDIA MAP ----
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


# ---- TAB 3: AI ANALYTICS ----
with tab3:
    st.markdown("### 🧠 Market Segmentation (K-Means Clustering)")
    # Using District-level data for AI analysis
    if not dist_df.empty:
        cluster_df = dist_df.groupby('district').agg({'amount': 'sum', 'count': 'sum'}).reset_index()
        X = StandardScaler().fit_transform(cluster_df[['amount', 'count']])
        cluster_df['cluster'] = KMeans(n_clusters=3, random_state=42, n_init=10).fit_predict(X)
        
        st.plotly_chart(render_pro_chart(cluster_df, 'count', 'amount', "District Tier Analysis", "Scatter", color='cluster'), use_container_width=True)
        st.markdown("""<div class="insight-box"><div class="insight-title">AI Interpretation</div>
        Districts are clustered into 3 tiers based on maturity. Upper-right districts represent high-velocity digital hubs.</div>""", unsafe_allow_html=True)

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

# ---- TAB 5: SQL INTELLIGENCE ----
# ---- TAB 5: SQL INTELLIGENCE (GLOBAL AGGREGATIONS) ----
with tab5:
    st.markdown("### 📂 Global SQL Aggregations")
    
    # Selection for visual aggregation
    t5_choice = st.selectbox("Visual Style", ["Bar", "Line"], key="t5_style")
    
    # 1. State Performance Query
    top_states_raw = pd.read_sql("SELECT state, SUM(amount) as total FROM aggregated_transaction GROUP BY state ORDER BY total DESC LIMIT 10", engine)
    
    # 2. Category Breakdown Query
    cat_perf_raw = pd.read_sql("SELECT category, SUM(amount) as total FROM aggregated_transaction GROUP BY category ORDER BY total DESC", engine)

    col_l, col_r = st.columns(2)
    
    with col_l:
        st.markdown("**Top 10 States by Revenue**")
        # Creating a display-friendly version of the dataframe
        top_states_disp = top_states_raw.copy()
        top_states_disp['total'] = top_states_disp['total'].apply(format_intl_amount)
        st.dataframe(top_states_disp, use_container_width=True, hide_index=True)
        
        # Original raw data used for plotting to keep axis values correct
        st.plotly_chart(render_pro_chart(top_states_raw, 'state', 'total', "", t5_choice), use_container_width=True)

    with col_r:
        st.markdown("**Transaction Category Split**")
        # Displaying formatted values
        cat_perf_disp = cat_perf_raw.copy()
        cat_perf_disp['total'] = cat_perf_disp['total'].apply(format_intl_amount)
        st.dataframe(cat_perf_disp, use_container_width=True, hide_index=True)
        
        st.plotly_chart(render_pro_chart(cat_perf_raw, 'category', 'total', "", t5_choice), use_container_width=True)

    # 3. Database Insights Box
    st.markdown(f"""
    <div class="insight-box">
        <div class="insight-title">Global DB Insights</div>
        <li><b>Highest Contributing State:</b> {top_states_raw.iloc[0]['state'].title()} ({format_intl_amount(top_states_raw.iloc[0]['total'])})</li>
        <li><b>Primary Driver:</b> {cat_perf_raw.iloc[0]['category']} transactions are currently the dominant revenue stream.</li>
    </div>
    """, unsafe_allow_html=True)
# ==========================================
# 6. FOOTER
# ==========================================
st.sidebar.markdown("---")
st.sidebar.write("📤 **Data Export**")
csv = df.to_csv(index=False).encode('utf-8')
st.sidebar.download_button("📩 Download Professional Report", data=csv, file_name=f"PhonePe_Insights_{selected_year}.csv", mime='text/csv')
st.sidebar.caption("Data Source: Multi-Level PhonePe Analytics (MySQL)")
st.markdown("<hr><center>Developed by Heena Kousar | Professional Edition v4.5</center>", unsafe_allow_html=True)
