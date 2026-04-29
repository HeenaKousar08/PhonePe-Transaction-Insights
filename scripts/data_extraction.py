import os
import json
import pandas as pd

path = "pulse/data/aggregated/transaction/country/india/state/"

data = []

for state in os.listdir(path):
    for year in os.listdir(f"{path}/{state}"):
        for file in os.listdir(f"{path}/{state}/{year}"):
            with open(f"{path}/{state}/{year}/{file}") as f:
                d = json.load(f)

                for i in d['data']['transactionData']:
                    data.append([
                        state,
                        int(year),
                        int(file.strip('.json')),
                        i['name'],
                        i['paymentInstruments'][0]['count'],
                        i['paymentInstruments'][0]['amount']
                    ])

df = pd.DataFrame(data, columns=[
    "state","year","quarter","category","count","amount"
])

df.to_csv("data/aggregated_transaction.csv", index=False)