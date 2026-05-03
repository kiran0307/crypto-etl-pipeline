import os
from pathlib import Path
from urllib.parse import quote_plus

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

server = os.getenv("AZURE_SQL_SERVER")
database = os.getenv("AZURE_SQL_DATABASE")
username = os.getenv("AZURE_SQL_USER")
password = quote_plus(os.getenv("AZURE_SQL_PASSWORD"))
driver = quote_plus(os.getenv("AZURE_SQL_DRIVER"))

connection_string = (
    f"mssql+pyodbc://{username}:{password}@{server}:1433/{database}"
    f"?driver={driver}&Encrypt=yes&TrustServerCertificate=no"
)

print("server:", server)
print("database:", database)
print("username:", username)
print("driver:", driver)
engine = create_engine(connection_string)

with engine.connect() as conn:
    result = conn.execute(text("SELECT @@VERSION")).scalar()
    print("✅ Connected to Azure SQL!")
    print(result)