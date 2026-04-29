import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from urllib.parse import quote_plus

# Connection (FIXED)
username = "heena"
password = quote_plus("Heena@08")

engine = create_engine(
    f"mysql+pymysql://{username}:{password}@127.0.0.1:3306/phonepe"
)

# Load data
query = "SELECT * FROM aggregated_transaction"
df = pd.read_sql(query, engine)

# Yearly Trend
year_data = df.groupby('year')['amount'].sum()

sns.lineplot(x=year_data.index, y=year_data.values)
plt.title("Yearly Transaction Trend")
plt.show()

# Category Distribution
cat_data = df.groupby('category')['amount'].sum()

cat_data.plot(kind='bar')
plt.title("Category Performance")
plt.show()