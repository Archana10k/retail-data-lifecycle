import pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib

DATA = Path(__file__).resolve().parents[2] / 'data' / 'processed' / 'daily_agg.parquet'
MODEL_DIR = Path(__file__).resolve().parents[2] / 'models'
MODEL_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_parquet(DATA)
X = df[['sales_7d_mean', 'sales_14d_mean', 'avg_price', 'promo_count']]
y = df['sales_qty']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestRegressor(n_estimators=50, random_state=42)
model.fit(X_train, y_train)

print("Test R²:", model.score(X_test, y_test))
joblib.dump(model, MODEL_DIR / 'rf_sales_model.pkl')
print("Model saved → rf_sales_model.pkl")
