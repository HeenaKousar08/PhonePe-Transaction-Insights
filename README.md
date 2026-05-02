# 📱 PhonePe AI-Powered Transaction Insights

![Python](https://img.shields.io/badge/Python-3.10-3776AB?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.25-FF4B4B?logo=streamlit)
![MySQL](https://img.shields.io/badge/MySQL-Database-4479A1?logo=mysql)
![Scikit-Learn](https://img.shields.io/badge/ML-Scikit--Learn-F7931E?logo=scikitlearn)

## 🚀 Overview
**PhonePe AI-Powered Transaction Insights** is a professional data analytics project that provides deep intelligence into digital transaction patterns across India. This project demonstrates a complete end-to-end data pipeline: **Raw JSON Extraction → Preprocessing → SQL Database → Interactive Dashboard → Machine Learning Insights.**

---

## 🎯 Objectives
* **Analyze** transaction trends across states and fiscal years.
* **Identify** top-performing states and spending categories using SQL.
* **Visualize** geographic distribution via high-fidelity India Choropleth maps.
* **Apply Machine Learning** for market segmentation (Clustering) and future forecasting.
* **Generate Business Insights** to understand digital payment maturity levels.

---

## 📊 Key Features

### 📉 Interactive Executive Dashboard
* **Real-time Metrics:** KPI cards for Total Value, Volume, and Average Ticket Size (ATS).
* **Customization:** Independent chart type selectors (Line/Bar/Area) for every tab.
* **Dynamic Filtering:** Filter by State and Year to drill down into specific regional data.

### 🌍 India Map Visualization
* **GeoJSON Integration:** Custom choropleth map for state-wise transaction comparisons.
* **Heatmap Logic:** Visualizes market saturation and the national digital divide.

### 🧠 AI Analytics (Machine Learning)
* **Market Segmentation:** Advanced **K-Means Clustering** using dual-features (Transaction Value + Volume) to identify market tiers.
* **Behavioral Analysis:** Groups states into "Dominant," "Growth," and "Emerging" clusters.

### 🔮 Predictive Forecasting
* **Polynomial Regression:** Models the non-linear growth of the digital economy.
* **Model Validation:** Features **Mean Absolute Error (MAE)** to quantify forecast reliability.
* **Future Outlook:** Generates data-driven projections through 2027.

### 📂 SQL Business Intelligence
* **Aggregated Insights:** Direct database queries for Category Performance and Yearly Trends.
* **Enterprise UI:** Clean, professional tables and charts for institutional-level reporting.

---

## 🛠️ Tech Stack
| Category | Tools Used |
| :--- | :--- |
| **Programming** | Python 3.10 |
| **Dashboard** | Streamlit (Custom CSS) |
| **Database** | MySQL / SQLAlchemy |
| **Visualization** | Plotly Express |
| **Machine Learning** | Scikit-learn (KMeans, LinearRegression) |
| **Data Handling** | Pandas, NumPy |

---

## 📂 Project Structure
```text
PhonePe-Transaction-Insights/
│
├── app/
│   ├── app.py                 # Main Streamlit Application
│   └── india_states.geojson   # GeoJSON for Map Visualization
│
├── assets/
│   ├── AIanalytics.png        # AI Tab Screenshot
│   ├── dashboard.png          # Dashboard Tab Screenshot
│   ├── indiamap.png           # Map Tab Screenshot
│   ├── prediction.png         # Forecast Tab Screenshot
│   ├── sqlintelligence.png    # SQL Tab Screenshot
│   └── footer.png             # UI Asset
│
├── data/                      # Standardized CSV files
├── scripts/
│   ├── data_extraction.py     # JSON to Dataframe conversion
│   └── load_to_sql.py         # MySQL Data Ingestion
│
├── requirements.txt           # Project Dependencies
└── README.md                  # Project Documentation


##⚙️ Installation & Setup

1️⃣ Clone Repository
Bash
git clone [https://github.com/HeenaKousar08/PhonePe-Transaction-Insights.git](https://github.com/HeenaKousar08/PhonePe-Transaction-Insights.git)
cd PhonePe-Transaction-Insights

2️⃣ Install Dependencies
Bash
pip install -r requirements.txt

3️⃣ Setup Database
Create a MySQL database named phonepe.

Update the credentials in app/app.py:

Python
username = "your_username"
password = "your_password"
Load the data using the ingestion script:

Bash
python scripts/load_to_sql.py

4️⃣ Run the Application
Bash
streamlit run app/app.py

📸 Dashboard Preview

🔹 Executive Dashboard
🔹 India Map Intelligence
🔹 AI Analytics & Clustering
🔹 Prediction Engine
🔹 SQL Business Intelligence

📈 Strategic Business Insights

Digital Maturity: Average Ticket Size (ATS) analysis reveals whether a state is a "High-Value" transfer hub or a "Retail Micro-payment" hub.

Saturation Points: Map insights identify states where merchant infrastructure is highly mature.

Market Tiers: Clustering helps businesses prioritize marketing spend based on high-volume vs high-value state behaviors.

👩‍💻 Author

Heena Kousar
Aspiring Data Analyst

⭐ If you find this project useful, please consider giving it a Star on GitHub!
