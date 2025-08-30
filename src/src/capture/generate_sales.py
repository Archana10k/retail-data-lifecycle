import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta

# Output folder for saving data
OUT = Path(__file__).resolve().parents[2] / 'data' / 'raw'
OUT.mkdir(parents=True, exist_ok=True)

np.random.seed(42)

# Example stores and products
stores = [f"store_{i}" for i in range(1, 6)]
products = [f"prod_{i:03d}" for i in range(1, 51)]
start = datetime(2024, 1, 1)
days = 10   # simulate 10 days of data

rows = []
for day in range(days):
    date = start + timedelta(days=day)
    for _ in range(200):  # 200 transactions per day
        store = np.random.choice(stores)
        product = np.random.choice(products)
        qty = int(np.random.poisson(1.5)) + 1
        price = round(np.random.uniform(5, 200), 2)
        promotion = np.random.choice([0, 1], p=[0.9, 0.1])
        ts = date + timedelta(seconds=int(np.random.uniform(0, 86400)))
        rows.append([ts, store, product, qty, price, promotion])

cols = ['timestamp', 'store_id', 'product_id', 'quantity', 'price', 'promotion']
df = pd.DataFrame(rows, columns=cols)

outfile = OUT / "sales.csv"
df.to_csv(outfile, index=False)
print('Wrote', outfile)
