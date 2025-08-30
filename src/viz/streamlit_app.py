import streamlit as st
import pandas as pd
import joblib
from pathlib import Path

st.title("📊 Retail Sales Dashboard")

DATA = Path(__file__).resolve().parents[2] / 'data' / 'processed' / 'daily_agg.parquet'
MODEL = Path(__file__).resolve().parents[2] / 'models' / 'rf_sales_model.pkl'

df = pd.read_parquet(DATA)
model = joblib.load(MODEL)

store = st.selectbox("Select Store", sorted(df['store_id'].unique()))
product = st.selectbox("Select Product", sorted(df['product_id'].unique()))

df_sub = df[(df['store_id'] == store) & (df['product_id'] == product)].sort_values('date')
st.line_chart(df_sub.set_index('date')['sales_qty'])

if st.button("Predict Next Day"):
    last = df_sub.iloc[-1]
    X = [[last['sales_7d_mean'], last['sales_14d_mean'], last['avg_price'], last['promo_count']]]
    pred = model.predict(X)[0]
    st.success(f"Predicted next-day sales: {pred:.1f}")
