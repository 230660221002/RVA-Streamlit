# Recommender Visibility Analyzer (RVA)

## Mitigasi Bias Algoritma pada Sistem Rekomendasi Marketplace Shopee untuk Mendukung Fairness Produk UMKM

Recommender Visibility Analyzer (RVA) merupakan sistem analisis berbasis data yang dirancang untuk membantu mengidentifikasi pengaruh popularitas produk dan rating terhadap visibilitas produk pada sistem rekomendasi marketplace Shopee. Sistem ini dikembangkan sebagai implementasi pendekatan Design Science Research (DSR) dengan fokus pada mitigasi bias algoritma dan peningkatan fairness exposure produk UMKM.

---

## Latar Belakang

Sistem rekomendasi pada marketplace digital seperti Shopee memanfaatkan berbagai parameter, seperti jumlah penjualan, jumlah ulasan, dan rating produk untuk menentukan produk yang muncul pada halaman rekomendasi.

Namun, sistem tersebut berpotensi menimbulkan *popularity bias*, yaitu kondisi ketika produk populer lebih sering direkomendasikan dibandingkan produk dari UMKM atau penjual baru. Akibatnya, distribusi visibilitas produk menjadi tidak seimbang.

RVA dikembangkan untuk membantu:
- menganalisis pola visibilitas produk,
- mendeteksi potensi bias algoritma,
- mendukung fairness produk UMKM,
- menyediakan visualisasi data rekomendasi marketplace.

---

## Fitur Utama

- Dashboard analisis visibilitas produk
- Visualisasi fairness produk UMKM
- Analisis hubungan popularitas dan rating
- Regresi linear sederhana
- Monitoring exposure produk
- Insight potensi bias algoritma

---

## Teknologi yang Digunakan

| Teknologi | Fungsi |
|---|---|
| Python | Pemrosesan data |
| Pandas | Manipulasi data |
| Streamlit | Dashboard interaktif |
| Matplotlib | Visualisasi data |
| Scikit-learn | Analisis regresi |
| Google Colab | Pengembangan awal |
| GitHub | Version control |
| Streamlit Cloud | Deployment aplikasi |

---

## Struktur Project

```bash
RVA-Streamlit/
│
├── app.py
├── data_observasi_shopee.csv
├── requirements.txt
└── README.md