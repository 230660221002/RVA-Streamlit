import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

st.set_page_config(
    page_title="RVA Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("Recommender Visibility Analyzer (RVA)")
st.write(
    "Dashboard analisis bias algoritma pada sistem rekomendasi marketplace Shopee "
    "untuk mendukung fairness produk UMKM."
)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("data_observasi_shopee.csv", sep=";")
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# Validasi kolom
required_columns = [
    "No",
    "Nama Produk",
    "Jumlah Terjual",
    "Jumlah Ulasan",
    "Rating",
    "Posisi Rekomendasi",
    "Frekuensi Muncul",
    "Jenis Toko"
]

missing_columns = [col for col in required_columns if col not in df.columns]

if missing_columns:
    st.error(f"Kolom berikut tidak ditemukan: {missing_columns}")
    st.write("Kolom yang terbaca:", df.columns.tolist())
    st.stop()

# Sidebar
st.sidebar.header("Filter Data")

jenis_toko = st.sidebar.multiselect(
    "Pilih Jenis Toko",
    options=df["Jenis Toko"].unique(),
    default=df["Jenis Toko"].unique()
)

df_filtered = df[df["Jenis Toko"].isin(jenis_toko)]

# Statistik ringkas
st.subheader("Ringkasan Data Observasi")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Produk", len(df_filtered))
col2.metric("Produk UMKM", len(df_filtered[df_filtered["Jenis Toko"] == "UMKM"]))
col3.metric("Toko Besar", len(df_filtered[df_filtered["Jenis Toko"] == "Toko Besar"]))
col4.metric("Rata-rata Rating", round(df_filtered["Rating"].mean(), 2))

# Data observasi
st.subheader("Data Observasi Produk")
st.dataframe(df_filtered, use_container_width=True)

# Grafik fairness UMKM vs Toko Besar
st.subheader("Perbandingan Frekuensi Muncul Berdasarkan Jenis Toko")

if not df_filtered.empty:
    avg_visibility = df_filtered.groupby("Jenis Toko")["Frekuensi Muncul"].mean()

    fig1, ax1 = plt.subplots()
    avg_visibility.plot(kind="bar", ax=ax1)
    ax1.set_xlabel("Jenis Toko")
    ax1.set_ylabel("Rata-rata Frekuensi Muncul")
    ax1.set_title("Rata-rata Frekuensi Muncul Produk")
    plt.xticks(rotation=0)
    st.pyplot(fig1)
else:
    st.warning("Data tidak tersedia berdasarkan filter yang dipilih.")

# Grafik posisi rekomendasi
st.subheader("Posisi Rekomendasi Produk")

fig2, ax2 = plt.subplots(figsize=(10, 5))
ax2.bar(df_filtered["Nama Produk"], df_filtered["Posisi Rekomendasi"])
ax2.set_xlabel("Nama Produk")
ax2.set_ylabel("Posisi Rekomendasi")
ax2.set_title("Posisi Rekomendasi Produk")
plt.xticks(rotation=75, ha="right")
st.pyplot(fig2)

st.caption(
    "Catatan: Semakin kecil nilai posisi rekomendasi, semakin tinggi posisi produk pada halaman rekomendasi."
)

# Analisis regresi linear
st.subheader("Analisis Regresi Linear")

X = df_filtered[["Jumlah Terjual", "Jumlah Ulasan", "Rating"]]
y = df_filtered["Frekuensi Muncul"]

if len(df_filtered) >= 3:
    model = LinearRegression()
    model.fit(X, y)

    coef_df = pd.DataFrame({
        "Variabel": X.columns,
        "Koefisien": model.coef_
    })

    st.dataframe(coef_df, use_container_width=True)

    col5, col6 = st.columns(2)
    col5.metric("Intercept", round(model.intercept_, 4))
    col6.metric("R² Score", round(model.score(X, y), 4))

    # Grafik koefisien regresi
    st.subheader("Visualisasi Koefisien Regresi")

    fig3, ax3 = plt.subplots()
    ax3.bar(coef_df["Variabel"], coef_df["Koefisien"])
    ax3.set_xlabel("Variabel")
    ax3.set_ylabel("Nilai Koefisien")
    ax3.set_title("Koefisien Regresi Linear")
    plt.xticks(rotation=0)
    st.pyplot(fig3)

    # Insight otomatis
    st.subheader("Insight Awal")

    top_coef = coef_df.sort_values(by="Koefisien", ascending=False).iloc[0]

    st.info(
        f"Variabel dengan pengaruh positif terbesar terhadap frekuensi kemunculan produk adalah "
        f"**{top_coef['Variabel']}** dengan koefisien sebesar **{top_coef['Koefisien']:.4f}**."
    )

    if model.score(X, y) >= 0.7:
        st.success(
            "Nilai R² menunjukkan bahwa model memiliki kemampuan penjelasan yang kuat terhadap "
            "variasi frekuensi kemunculan produk."
        )
    else:
        st.warning(
            "Nilai R² masih rendah, sehingga diperlukan data tambahan atau variabel lain untuk meningkatkan kualitas model."
        )

else:
    st.warning("Jumlah data terlalu sedikit untuk melakukan analisis regresi.")

# Analisis fairness sederhana
st.subheader("Analisis Fairness Produk UMKM")

if "UMKM" in df_filtered["Jenis Toko"].values and "Toko Besar" in df_filtered["Jenis Toko"].values:
    avg_umkm = df_filtered[df_filtered["Jenis Toko"] == "UMKM"]["Frekuensi Muncul"].mean()
    avg_big = df_filtered[df_filtered["Jenis Toko"] == "Toko Besar"]["Frekuensi Muncul"].mean()

    st.write(f"Rata-rata frekuensi muncul produk UMKM: **{avg_umkm:.2f}**")
    st.write(f"Rata-rata frekuensi muncul produk Toko Besar: **{avg_big:.2f}**")

    if avg_big > avg_umkm:
        st.warning(
            "Produk dari Toko Besar memiliki rata-rata frekuensi kemunculan lebih tinggi dibandingkan UMKM. "
            "Hal ini menunjukkan adanya indikasi ketimpangan exposure produk."
        )
    elif avg_umkm > avg_big:
        st.success(
            "Produk UMKM memiliki rata-rata frekuensi kemunculan lebih tinggi dibandingkan Toko Besar."
        )
    else:
        st.info(
            "Rata-rata frekuensi kemunculan produk UMKM dan Toko Besar relatif seimbang."
        )
else:
    st.info("Analisis fairness membutuhkan data UMKM dan Toko Besar secara bersamaan.")

# Rekomendasi mitigasi
st.subheader("Rekomendasi Mitigasi Bias Algoritma")

mitigation_data = {
    "Area Risiko": [
        "Bias Algoritma",
        "Ketimpangan Exposure",
        "Dominasi Produk Populer",
        "Privasi Data"
    ],
    "Strategi Teknis": [
        "Audit algoritma dan monitoring fairness rekomendasi",
        "Diversifikasi parameter rekomendasi produk",
        "Penyesuaian bobot algoritma",
        "Anonimisasi data observasi"
    ],
    "Strategi Kebijakan/Manajerial": [
        "Pembentukan kebijakan fairness recommendation",
        "Transparansi sistem rekomendasi",
        "Pengawasan internal marketplace",
        "Kebijakan perlindungan data pengguna"
    ]
}

mitigation_df = pd.DataFrame(mitigation_data)
st.dataframe(mitigation_df, use_container_width=True)

st.markdown("---")
st.caption(
    "RVA dikembangkan untuk kebutuhan akademik dalam menganalisis bias algoritma "
    "pada sistem rekomendasi marketplace dan mendukung fairness produk UMKM."
)