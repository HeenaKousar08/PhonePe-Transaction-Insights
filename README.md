📱 PhonePe Intelligence Pro – AI-Powered Transaction Insights
🚀 Overview

PhonePe Intelligence Pro is an advanced analytics dashboard built using Streamlit that delivers deep insights into digital payment trends across India.

This project combines:

📊 Interactive data visualization
🧠 Machine learning analytics
🗄️ SQL-based aggregation
🔮 Predictive modeling

to transform raw transaction data into actionable business intelligence.

🎯 Objectives
Analyze transaction patterns across states and years
Provide interactive dashboards for business decision-making
Visualize geographical distribution using India map
Apply machine learning for segmentation & forecasting
Extract insights directly from SQL database queries
📊 Key Features
📉 1. Interactive Dashboard
State & Year filters
KPI metrics:
Total Transaction Value
Transaction Volume
Average Ticket Size
Dynamic charts (Line / Bar / Area)
🌍 2. India Map Visualization
Choropleth map of India
State-wise transaction distribution
Identifies top-performing regions
Highlights digital adoption gaps
🧠 3. AI Analytics (Machine Learning)
K-Means Clustering
Segments states into behavioral groups
Uses:
Transaction Amount
Transaction Count
Helps identify:
High-value markets
Emerging regions
🔮 4. Predictions (Forecasting)
Polynomial Regression Model
Predicts future transaction trends (2025–2027)
Shows:
Growth trajectory
Market expansion patterns
📂 5. SQL Intelligence
Real-time database insights using SQL
Key analysis:
🏆 Top performing states
📂 Category-wise performance
Interactive tables + charts
📥 6. Data Export
Download dataset as CSV
Useful for reporting & further analysis
🛠️ Tech Stack
Category	Tools Used
Programming	Python
Dashboard	Streamlit
Database	MySQL (via SQLAlchemy & PyMySQL)
Visualization	Plotly
Machine Learning	Scikit-learn
Data Handling	Pandas
📂 Project Structure
PhonePe-Transaction-Insights/
│
├── app.py                     # Main Streamlit App
├── phonepe.db / MySQL DB     # Database
├── india_states.geojson      # Map file
├── notebooks/
│   └── analysis.ipynb        # Data analysis & ML
├── requirements.txt
└── README.md
⚙️ Installation & Setup
1️⃣ Clone Repository
git clone https://github.com/HeenaKousar08/PhonePe-Transaction-Insights.git
cd PhonePe-Transaction-Insights
2️⃣ Install Dependencies
pip install -r requirements.txt
3️⃣ Setup MySQL Database
Create database:
CREATE DATABASE phonepe;
Import your dataset into:
aggregated_transaction
4️⃣ Run the Application
streamlit run app.py
📈 Business Insights
📊 Digital transactions show strong upward growth
🌍 Certain states dominate in transaction value & volume
🧠 AI clustering reveals:
High-growth markets
Underperforming regions
🔮 Forecasting indicates continued expansion of digital payments
⚠️ Challenges Solved
Fixed SQL column mismatch (category vs transaction_type)
Resolved Streamlit tab rendering issues
Optimized ML pipeline for better insights
Handled database integration errors
🔮 Future Enhancements
Real-time data integration (API-based)
Advanced ML models (XGBoost, Prophet)
District-level analytics
Cloud deployment (AWS / Streamlit Cloud)
User authentication system
📸 Dashboard Preview
🔹 Main Dashboard

(Add your screenshot here)

assets/dashboard.png
👩‍💻 Author

Heena Kousar
Aspiring Data Analyst | Python | SQL | Machine Learning

📜 License

This project is open-source under the MIT License

⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub!