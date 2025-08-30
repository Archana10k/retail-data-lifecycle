import pandas as pd
from pathlib import Path
import sqlite3

DB = Path(__file__).resolve().parents[2] / 'data' / 'database' / 'sales.db'
OUT = Path(__file__).resolve().parents[2] / 'data' / 'processed'
OUT.mkdir(parents=True, exist_ok=True)

# Read from SQLite
con = sqlite3.connect(DB)
df = pd.read_sql('SELECT * FROM raw_sales', con, parse_dates=['timestamp'])
con.close()

# Aggregate to daily level
df['date'] = df['timestamp'].dt.floor('d')
agg = df.groupby(['date', 'store_id', 'product_id']).agg(
    sales_qty=('quantity', 'sum'),
    avg_price=('price', 'mean'),
    promo_count=('promotion', 'sum')
).reset_index()

# Rolling features
agg = agg.sort_values(['store_id', 'product_id', 'date'])
agg['sales_7d_mean'] = agg.groupby(['store_id', 'product_id'])['sales_qty'].transform(lambda x: x.rolling(7, min_periods=1).mean())
agg['sales_14d_mean'] = agg.groupby(['store_id', 'product_id'])['sales_qty'].transform(lambda x: x.rolling(14, min_periods=1).mean())

agg.to_parquet(OUT / 'daily_agg.parquet', index=False)
print('Wrote →', OUT / 'daily_agg.parquet')
