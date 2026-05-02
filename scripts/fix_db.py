import os
import json
import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus

# 1. Database Connection
username = "heena"
password = quote_plus("Heena@08")
engine = create_engine(f"mysql+pymysql://{username}:{password}@127.0.0.1:3306/phonepe")

def push_final_data():
    # --- PART 1: MAP TRANSACTION (Already done, but safe to run again) ---
    map_path = "pulse/data/map/transaction/hover/country/india/state/"
    map_list = []
    for state in os.listdir(map_path):
        s_p = os.path.join(map_path, state)
        for yr in os.listdir(s_p):
            y_p = os.path.join(s_p, yr)
            for f_name in os.listdir(y_p):
                with open(os.path.join(y_p, f_name), 'r') as f:
                    d = json.load(f)
                    for i in d['data']['hoverDataList']:
                        map_list.append([state, int(yr), int(f_name.strip('.json')), i['name'], i['metric'][0]['count'], i['metric'][0]['amount']])
    
    pd.DataFrame(map_list, columns=["state", "year", "quarter", "district", "count", "amount"]).to_sql('map_transaction', engine, if_exists='replace', index=False)
    print("✅ map_transaction synced.")

    # --- PART 2: TOP TRANSACTION (PINCODES) - THE MISSING PIECE ---
    top_path = "pulse/data/top/transaction/country/india/state/"
    top_list = []
    for state in os.listdir(top_path):
        s_p = os.path.join(top_path, state)
        for yr in os.listdir(s_p):
            y_p = os.path.join(s_p, yr)
            for f_name in os.listdir(y_p):
                with open(os.path.join(y_p, f_name), 'r') as f:
                    d = json.load(f)
                    for i in d['data']['pincodes']:
                        top_list.append([state, int(yr), int(f_name.strip('.json')), i['entityName'], i['metric']['count'], i['metric']['amount']])
    
    pd.DataFrame(top_list, columns=["state", "year", "quarter", "pincode", "count", "amount"]).to_sql('top_transaction_pincode', engine, if_exists='replace', index=False)
    print("✅ top_transaction_pincode synced.")

if __name__ == "__main__":
    push_final_data()
    print("\n🚀 DATABASE FULLY ARMED AND READY!")