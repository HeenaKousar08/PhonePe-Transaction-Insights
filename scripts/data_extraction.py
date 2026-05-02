import os
import json
import pandas as pd

# --- 1. EXTRACT MAP TRANSACTION (DISTRICTS) ---
map_path = "pulse/data/map/transaction/hover/country/india/state/"
map_data = []

for state in os.listdir(map_path):
    state_path = os.path.join(map_path, state)
    for year in os.listdir(state_path):
        year_path = os.path.join(state_path, year)
        for file in os.listdir(year_path):
            with open(os.path.join(year_path, file), 'r') as f:
                d = json.load(f)
                for i in d['data']['hoverDataList']:
                    map_data.append([
                        state, int(year), int(file.strip('.json')),
                        i['name'], # This is the District Name
                        i['metric'][0]['count'],
                        i['metric'][0]['amount']
                    ])

map_df = pd.DataFrame(map_data, columns=["state", "year", "quarter", "district", "count", "amount"])
map_df.to_csv("data/map_transaction.csv", index=False)

# --- 2. EXTRACT TOP TRANSACTION (PINCODES) ---
top_path = "pulse/data/top/transaction/country/india/state/"
top_data = []

for state in os.listdir(top_path):
    state_path = os.path.join(top_path, state)
    for year in os.listdir(state_path):
        year_path = os.path.join(state_path, year)
        for file in os.listdir(year_path):
            with open(os.path.join(year_path, file), 'r') as f:
                d = json.load(f)
                for i in d['data']['pincodes']:
                    top_data.append([
                        state, int(year), int(file.strip('.json')),
                        i['entityName'], # This is the Pincode
                        i['metric']['count'],
                        i['metric']['amount']
                    ])

top_df = pd.DataFrame(top_data, columns=["state", "year", "quarter", "pincode", "count", "amount"])
top_df.to_csv("data/top_transaction_pincode.csv", index=False)