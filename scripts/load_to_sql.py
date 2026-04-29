from sqlalchemy import create_engine
from urllib.parse import quote_plus

username = "heena"
password = quote_plus("Heena@08")

engine = create_engine(
    f"mysql+pymysql://{username}:{password}@127.0.0.1:3306/phonepe"
)