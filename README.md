# 📱 PhonePe AI-Powered Transaction Insights

## 🚀 Overview

**PhonePe AI-Powered Transaction Insights** is an advanced interactive data analytics dashboard built using Streamlit. It provides deep insights into digital transaction patterns across India by integrating data visualization, SQL-based querying, and machine learning models.

This project showcases a complete data pipeline — from raw JSON data extraction and database storage to real-time analytics, visualization, anomaly detection, and future forecasting.

---

## 🎯 Objectives

* Analyze transaction trends across states, years, and categories  
* Build an interactive dashboard for business intelligence  
* Visualize geographical distribution of transactions across India  
* Detect anomalies in transaction patterns using AI  
* Predict future transaction trends using machine learning  

---

## 📊 Key Features

### 📍 Interactive Dashboard

* Dynamic filters for **State** and **Year**
* KPI metrics:
  - Total Transaction Amount 💰
  - Total Transactions 📊
  - Average Transaction Value 📈
* Multiple chart types (Line / Bar / Area)

---

### 📈 Data Visualization

* Yearly transaction trends  
* Category-wise performance analysis  
* State-level comparisons  
* Clean and responsive UI using Plotly  

---

### 🌍 India State-wise Map

* Choropleth map for geographic insights  
* State-wise transaction distribution  
* Highlights regional digital adoption patterns  

---

### 🧠 Machine Learning Insights

* **K-Means Clustering** → Market segmentation of states  
* **Isolation Forest** → Anomaly detection in transaction trends  
* Identifies unusual spikes or drops in data  

---

### 🔮 Prediction & Forecasting

* **Polynomial Regression** → Future transaction prediction  
* **Prophet Model (optional)** → Advanced time-series forecasting  
* Forecasts trends for upcoming years  

---

### 📁 SQL Insights

* Top 10 states by transaction amount  
* Category-wise transaction performance  
* Yearly transaction growth trends  
* Direct SQL queries integrated into dashboard  

---

### 📥 Data Export

* Download dataset as CSV directly from dashboard  

---

## 🛠️ Tech Stack

| Category        | Tools Used                         |
| --------------- | ---------------------------------- |
| Programming     | Python                             |
| Dashboard       | Streamlit                          |
| Database        | MySQL / SQLite                     |
| Visualization   | Plotly, Matplotlib, Seaborn        |
| Machine Learning| Scikit-learn, Prophet              |
| Data Handling   | Pandas, NumPy                      |
| Version Control | Git & GitHub                       |

---

## 📂 Project Structure

PhonePe-Transaction-Insights/
│
├── app.py                        # Main Streamlit dashboard
├── phonepe.db / MySQL DB         # Database
├── india_states.geojson          # Map file
├── requirements.txt
├── README.md
│
├── assets/
│   ├── dashboard.png
│   ├── map.png
│   └── prediction.png
│
├── notebooks/
│   └── analysis.ipynb            # Data analysis & ML


---## ⚙️ Installation & Setup###

1️⃣ Clone the Repository
 ```bashgit clone https://github.com/HeenaKousar08/PhonePe-Transaction-Insights.gitcd PhonePe-Transaction-Insights

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Setup Database
Option 1: MySQL


Create database: phonepe


Load dataset into table: aggregated_transaction


Option 2: SQLite (Recommended for simplicity)


Use phonepe.db file directly



4️⃣ Run the Application
streamlit run app.py

📈 Business Insights


Strong growth in digital transactions across years 📈


Certain states dominate the digital payment ecosystem


Category analysis reveals consumer spending behavior


Anomaly detection highlights unusual transaction spikes


Forecasting helps predict future digital payment trends



🔮 Future Enhancements


Real-time data integration


Advanced ML models (XGBoost, Deep Learning)


Cloud deployment (AWS / Streamlit Cloud)


District-level analysis


Enhanced UI/UX with animations



📸 Dashboard Preview


🔹 Main Dashboard

🔹 India Map

🔹 Prediction


👩‍💻 Author
Heena Kousar
Aspiring Data Analyst | Python | SQL | Machine Learning

📜 License
This project is open-source and available under the MIT License.

⭐ Support
If you like this project, consider giving it a ⭐ on GitHub!
