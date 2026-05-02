import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus

# 1. Connection Setup
username = "heena"
password = quote_plus("Heena@08")
engine = create_engine(f"mysql+pymysql://{username}:{password}@127.0.0.1:3306/phonepe")

# 2. Load CSVs into DataFrames 
# (Make sure these CSVs were created by your data_extraction.py)
agg_df = pd.read_csv("data/aggregated_transaction.csv")
map_df = pd.read_csv("data/map_transaction.csv")
top_df = pd.read_csv("data/top_transaction_pincode.csv")

# 3. Push to MySQL
try:
    agg_df.to_sql('aggregated_transaction', engine, if_exists='replace', index=False)
    map_df.to_sql('map_transaction', engine, if_exists='replace', index=False)
    top_df.to_sql('top_transaction_pincode', engine, if_exists='replace', index=False)
    print("✅ All tables (Aggregated, Map, Top) successfully uploaded to MySQL!")
except Exception as e:
    print(f"❌ Error uploading to SQL: {e}")