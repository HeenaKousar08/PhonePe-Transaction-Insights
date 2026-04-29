import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus
import plotly.express as px
from sklearn.linear_model import LinearRegression

# ---- PAGE CONFIG ----
st.set_page_config(
    page_title="PhonePe Analytics Dashboard",
    page_icon="📱",
    layout="wide"
)

# ---- CUSTOM LIGHT UI ----
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background-color: #F5F6FA;
}
[data-testid="stSidebar"] {
    background-color: #FFFFFF;
}
.metric-card {
    background: white;
    padding: 18px;
    border-radius: 12px;
    text-align: center;
    border: 1px solid #E5E7EB;
    box-shadow: 0px 3px 8px rgba(0,0,0,0.05);
}
h1 {
    color: #5F259F;
}
</style>
""", unsafe_allow_html=True)

# ---- DATABASE ----
@st.cache_resource
def get_engine():
    username = "heena"
    password = quote_plus("Heena@08")
    return create_engine(
        f"mysql+pymysql://{username}:{password}@127.0.0.1:3306/phonepe"
    )

engine = get_engine()

# ---- LOAD DATA ----
@st.cache_data
def load_data():
    return pd.read_sql("SELECT * FROM aggregated_transaction", engine)

df = load_data()
df['state'] = df['state'].str.lower()

# ---- SIDEBAR ----
st.sidebar.title("🔍 Filters")
state = st.sidebar.selectbox("Select State", sorted(df['state'].unique()))
year = st.sidebar.selectbox("Select Year", sorted(df['year'].unique()))

filtered_df = df[(df['state'] == state) & (df['year'] == year)]

# ---- ADVANCED FILTER (NEW) ----
st.sidebar.markdown("### ⚙ Advanced Filters")

multi_states = st.sidebar.multiselect(
    "Select Multiple States",
    df['state'].unique()
)

if multi_states:
    filtered_df = df[(df['state'].isin(multi_states)) & (df['year'] == year)]

# ---- HEADER ----
st.markdown("""
<style>
.header-container {
    text-align: center;
    padding: 25px 10px;
}

.header-title {
    font-size: 38px;
    font-weight: 700;
    color: #5F259F;
    margin-bottom: 8px;
}

.header-subtitle {
    font-size: 16px;
    color: #6B7280;
    margin-bottom: 15px;
}

.logo {
    width: 70px;
    margin-bottom: 10px;
}

.divider {
    height: 1px;
    background: linear-gradient(to right, transparent, #D1D5DB, transparent);
    margin-top: 10px;
    margin-bottom: 20px;
}
</style>

<div class="header-container">
    <img class="logo" src="https://download.logo.wine/logo/PhonePe/PhonePe-Logo.wine.png">
    <div class="header-title">PhonePe AI-Powered Transaction Insights</div>
    <div class="header-subtitle">
        Real-time insights, predictive analytics, and anomaly detection for digital transactions
    </div>
</div>

<div class="divider"></div>
""", unsafe_allow_html=True)
# ---- KPI ----
total_amount = filtered_df['amount'].sum()
total_transactions = len(filtered_df)
avg_transaction = filtered_df['amount'].mean()

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"<div class='metric-card'><h3>💰 Total Amount</h3><h2>₹ {total_amount:,.0f}</h2></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='metric-card'><h3>📊 Transactions</h3><h2>{total_transactions}</h2></div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div class='metric-card'><h3>📈 Avg Transaction</h3><h2>₹ {avg_transaction:,.0f}</h2></div>", unsafe_allow_html=True)

    # ---- KPI GROWTH (NEW) ----
prev_year = year - 1
prev_data = df[(df['state'] == state) & (df['year'] == prev_year)]

if not prev_data.empty:
    prev_amount = prev_data['amount'].sum()
    growth = ((total_amount - prev_amount) / prev_amount) * 100 if prev_amount != 0 else 0

    st.metric("📈 YoY Growth", f"{growth:.2f}%", delta=f"{growth:.2f}%")

# ---- TREND ----
st.markdown("## 📈 Trends")

chart_type = st.selectbox("Select Trend Chart", ["Line", "Bar", "Area"])

year_data = df[df['state'] == state].groupby('year')['amount'].sum().reset_index()

if chart_type == "Line":
    fig1 = px.line(year_data, x='year', y='amount', markers=True)
elif chart_type == "Bar":
    fig1 = px.bar(year_data, x='year', y='amount')
else:
    fig1 = px.area(year_data, x='year', y='amount')

st.plotly_chart(fig1, use_container_width=True)

# ---- ANOMALY DETECTION ----
st.markdown("## 🚨 Anomaly Detection")

year_data['z_score'] = (year_data['amount'] - year_data['amount'].mean()) / year_data['amount'].std()

anomalies = year_data[abs(year_data['z_score']) > 1.5]

fig_anomaly = px.scatter(year_data, x='year', y='amount',
                         color=year_data['z_score'].abs() > 1.5,
                         title="Anomaly Detection")

st.plotly_chart(fig_anomaly, use_container_width=True)

if not anomalies.empty:
    st.warning(f"⚠ Detected {len(anomalies)} unusual spikes in data")

# ---- GROWTH ----
year_data['growth'] = year_data['amount'].pct_change() * 100

fig2 = px.bar(year_data, x='year', y='growth', title="Growth Rate (%)")
st.plotly_chart(fig2, use_container_width=True)

# ---- INSIGHTS ----
st.markdown("## 🏆 Insights")

# ---- DEFINE TOP STATE (FIX) ----
top_state = df.groupby('state')['amount'].sum().idxmax()

# ---- SMART INSIGHTS ----
st.markdown("## 🧠 Smart Insights")


growth_text = ""

if len(year_data) > 1:
    first = year_data.iloc[0]['amount']
    last = year_data.iloc[-1]['amount']
    change = ((last - first) / first) * 100 if first != 0 else 0

    growth_text = f"📊 Transactions changed by {change:.2f}% over the years."

top3 = df.groupby('state')['amount'].sum().nlargest(3)
contribution = (top3.sum() / df['amount'].sum()) * 100

st.info(f"""
{growth_text}

🏆 Top 3 states contribute **{contribution:.2f}%** of total transactions.

🚀 Highest performing state: **{top_state.upper()}**
""")

# Top states chart switch
chart_type2 = st.selectbox("Top States Chart Type", ["Bar", "Horizontal Bar"])

top_states = df.groupby('state')['amount'].sum().nlargest(10).reset_index()

if chart_type2 == "Bar":
    fig3 = px.bar(top_states, x='state', y='amount')
else:
    fig3 = px.bar(top_states, x='amount', y='state', orientation='h')

st.plotly_chart(fig3, use_container_width=True)

# Category chart switch
if 'category' in df.columns:
    chart_type3 = st.selectbox("Category Chart Type", ["Pie", "Bar"])
    cat_data = df.groupby('category')['amount'].sum().reset_index()

    if chart_type3 == "Pie":
        fig4 = px.pie(cat_data, names='category', values='amount')
    else:
        fig4 = px.bar(cat_data, x='category', y='amount')

    st.plotly_chart(fig4, use_container_width=True)

# ---- ML ----
# ---- ML UPGRADE ----
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

st.markdown("## 🔮 Future Prediction (Advanced)")

model = make_pipeline(PolynomialFeatures(degree=2), LinearRegression())
model.fit(year_data[['year']], year_data['amount'])

future = pd.DataFrame({'year': [2025, 2026, 2027]})
future['prediction'] = model.predict(future)

# Combine actual + predicted
combined = pd.concat([
    year_data.rename(columns={'amount': 'value'})[['year', 'value']],
    future.rename(columns={'prediction': 'value'})
])

fig5 = px.line(combined, x='year', y='value', markers=True,
               title="Actual + Predicted Trend")

st.plotly_chart(fig5, use_container_width=True)

# ---- CLEAN STATE NAMES ----
df['state_clean'] = (
    df['state']
    .str.replace("-", " ", regex=False)
    .str.replace("&", "and", regex=False)
    .str.strip()
    .str.title()
)

# ---- MANUAL FIXES (IMPORTANT FOR INDIA DATA) ----
state_mapping = {
    "Andaman And Nicobar Islands": "Andaman and Nicobar Islands",
    "Dadra And Nagar Haveli And Daman And Diu": "Dadra and Nagar Haveli and Daman and Diu",
    "Nct Of Delhi": "Delhi",
    "Jammu And Kashmir": "Jammu & Kashmir"
}

df['state_clean'] = df['state_clean'].replace(state_mapping)

# ---- LOAD GEOJSON ----
import json, os

st.markdown("## 🌍 India Map")

geo_path = os.path.join(os.path.dirname(__file__), "india_states.geojson")

with open(geo_path) as f:
    geojson = json.load(f)

# ---- AUTO DETECT GEOJSON KEY (🔥 MAIN FIX) ----
sample_props = geojson['features'][0]['properties']
possible_keys = ['ST_NM', 'state', 'NAME_1', 'name']

KEY = None
for k in possible_keys:
    if k in sample_props:
        KEY = k
        break

if KEY is None:
    st.error("❌ Could not find matching key in GeoJSON")
    st.stop()

# ---- EXTRACT GEO STATES ----
geo_states = [f['properties'][KEY] for f in geojson['features']]

# ---- MAP DATA ----
map_data = df.groupby('state_clean')['amount'].sum().reset_index()

# ---- FILTER MATCHING STATES ONLY ----
map_data = map_data[map_data['state_clean'].isin(geo_states)]

# ---- CHOROPLETH ----
import plotly.express as px

fig_map = px.choropleth(
    map_data,
    geojson=geojson,
    featureidkey=f"properties.{KEY}",
    locations="state_clean",
    color="amount",
    color_continuous_scale="Turbo"
)

fig_map.update_geos(fitbounds="locations", visible=False)

st.plotly_chart(fig_map, use_container_width=True)

# ---- INSIGHT ----
top_state = df.groupby('state')['amount'].sum().idxmax()
st.success(f"🚀 Highest transaction state: {top_state.upper()}")

# ---- STATE COMPARISON ----
st.markdown("## ⚖ Compare States")

state1 = st.selectbox("Select State 1", df['state'].unique(), key="s1")
state2 = st.selectbox("Select State 2", df['state'].unique(), key="s2")

comp = df[df['state'].isin([state1, state2])]

comp_data = comp.groupby(['year', 'state'])['amount'].sum().reset_index()

fig_comp = px.line(comp_data, x='year', y='amount', color='state',
                   markers=True, title="State Comparison")

st.plotly_chart(fig_comp, use_container_width=True)

# ---- DOWNLOAD ----
st.download_button(
    "⬇ Download Data",
    data=filtered_df.to_csv(index=False),
    file_name="phonepe_data.csv"
)

# ---- EXPORT EXCEL ----
import io

buffer = io.BytesIO()
filtered_df.to_excel(buffer, index=False)

st.download_button(
    label="⬇ Download Excel",
    data=buffer,
    file_name="phonepe_data.xlsx",
    mime="application/vnd.ms-excel"
)

# ---- FOOTER ----
st.markdown("---")

st.markdown(
    """
    <div style='text-align: center; color: gray; font-size: 14px;'>
        <p>📱 <b>PhonePe Transaction Dashboard</b></p>
        <p>Developed by Heena Kousar</p>
        <p>Built using Python, SQL, Streamlit & Machine Learning</p>
        <p>© 2026 All Rights Reserved</p>
    </div>
    """,
    unsafe_allow_html=True
)