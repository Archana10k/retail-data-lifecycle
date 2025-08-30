import sqlite3
import pandas as pd
from pathlib import Path

RAW = Path(__file__).resolve().parents[2] / 'data' / 'raw'
DB_DIR = Path(__file__).resolve().parents[2] / 'data' / 'database'
DB_DIR.mkdir(parents=True, exist_ok=True)
DB = DB_DIR / 'sales.db'

con = sqlite3.connect(DB)
for csv in RAW.glob('*.csv'):
    df = pd.read_csv(csv, parse_dates=['timestamp'])
    df.to_sql('raw_sales', con, if_exists='append', index=False)
con.close()

print('Ingest completed →', DB)
