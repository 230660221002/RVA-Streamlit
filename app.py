import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

st.set_page_config(page_title="RVA Dashboard", layout="wide")

st.title("Recommender Visibility Analyzer (RVA)")
st.write("Dashboard analisis fairness visibilitas produk UMKM pada marketplace Shopee.")

df = pd.read_csv("data_observasi_shopee.csv", sep=";")
df.columns = df.columns.str.strip()

st.subheader("Data Observasi Produk")
st.dataframe(df)

col1, col2, col3 = st.columns(3)
col1.metric("Total Produk", len(df))
col2.metric("Produk UMKM", len(df[df["Jenis Toko"] == "UMKM"]))
col3.metric("Toko Besar", len(df[df["Jenis Toko"] == "Toko Besar"]))

st.subheader("Rata-rata Frekuensi Muncul Berdasarkan Jenis Toko")
avg_freq = df.groupby("Jenis Toko")["Frekuensi Muncul"].mean()

fig, ax = plt.subplots()
avg_freq.plot(kind="bar", ax=ax)
ax.set_xlabel("Jenis Toko")
ax.set_ylabel("Rata-rata Frekuensi Muncul")
st.pyplot(fig)

st.subheader("Analisis Regresi Linear")
X = df[["Jumlah Terjual", "Jumlah Ulasan", "Rating"]]
y = df["Frekuensi Muncul"]

model = LinearRegression()
model.fit(X, y)

coef_df = pd.DataFrame({
    "Variabel": X.columns,
    "Koefisien": model.coef_
})

st.dataframe(coef_df)

st.write("Intercept:", model.intercept_)
st.write("R² Score:", model.score(X, y))

st.subheader("Insight Awal")
st.info(
    "Jika koefisien jumlah terjual, jumlah ulasan, atau rating bernilai positif, "
    "maka variabel tersebut berpotensi meningkatkan frekuensi kemunculan produk dalam sistem rekomendasi."
)
