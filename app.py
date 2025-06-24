# ====================== IMPORT LIBRARY ======================

import streamlit as st                      # Streamlit untuk membuat UI web interaktif
import pandas as pd                        # Pandas untuk manipulasi data
from sklearn.cluster import KMeans         # KMeans untuk algoritma clustering
from sklearn.preprocessing import StandardScaler  # Normalisasi data

# ====================== KONFIGURASI HALAMAN ======================
st.set_page_config(page_title="Rekomendasi Jurusan Kuliah", layout="centered") # Set judul dan layout halaman

# Styling tambahan menggunakan CSS agar tampilan lebih menarik
st.markdown("""
    <style>
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            padding-left: 3vw !important;
            padding-right: 3vw !important;
            max-width: none !important;
            width: 100% !important;
        }

        section[data-testid="column"] > div {
            padding-left: 1vw;
            padding-right: 1vw;
        }

        .stSlider > div > div {
            background-color: #ffecec;
            padding: 0.5rem;
            border-radius: 10px;
        }

        .stButton>button {
            background-color: #f63366;
            color: white;
            font-weight: bold;
            padding: 0.5rem 1rem;
            border-radius: 10px;
        }

        html, body, [class*="css"]  {
            font-size: 1.1rem;
        }
    </style>
""", unsafe_allow_html=True)

# ====================== FUNGSI LOAD DATA ======================
# Fungsi load data dari GitHub
@st.cache_data
def load_data(jurusan_sma):
    # Menentukan URL file CSV berdasarkan jurusan SMA
    if jurusan_sma == "IPA":
        url = "https://raw.githubusercontent.com/digitalperspektif/rekomendasi-jurusan/main/data_ipa.csv"
    else:
        url = "https://raw.githubusercontent.com/digitalperspektif/rekomendasi-jurusan/main/data_ips.csv"
    
    # Membaca data dan membersihkan spasi putih
    df = pd.read_csv(url)
    df["Minat"] = df["Minat"].astype(str).str.strip()
    df["Jurusan"] = df["Jurusan"].astype(str).str.strip()
    
    # Menghapus baris yang mengandung data kosong
    return df.dropna()


# ====================== JUDUL DAN LAYOUT ======================
# Judul aplikasi
st.title("🎓 Rekomendasi Jurusan Kuliah")

# Dua kolom layout
col1, col2 = st.columns([1, 1.2])

# ====================== KOLOM KIRI: PENJELASAN ======================
with col1:
    # Penjelasan tentang aplikasi
    st.markdown("## 📖 Tentang Aplikasi")
    st.markdown("""
    Aplikasi **Rekomendasi Jurusan Kuliah Untuk Siswa SMA Berdasarkan Minat dan Nilai Akademik Menggunakan K-Means Clustering** bertujuan untuk
    merekomendasikan jurusan kuliah berdasarkan **nilai akademik** dan **minat utama** kamu.

    Silakan pilih jurusan SMA terlebih dahulu (IPA atau IPS), lalu isi nilai pelajaran dan pilih minat.
    """)

    # Penjelasan tentang cara kerja KMeans
    st.markdown("---")
    st.markdown("### 🧠 Cara Kerja Algoritma K-Means")
    st.markdown("""
    Algoritma **K-Means Clustering** digunakan untuk mengelompokkan data jurusan berdasarkan kesamaan pola nilai pelajaran dan minat.  
    Berikut langkah-langkah utamanya:

    1. **Preprocessing Data**  
       Nilai dan minat dikonversi menjadi format numerik & dinormalisasi.
    
    2. **Clustering dengan K-Means**  
       Data dikelompokkan menjadi 3 cluster utama berdasarkan pola kemiripan.
    
    3. **Prediksi Cluster Pengguna**  
       Sistem menempatkan kamu ke salah satu cluster berdasarkan input.
    
    4. **Rekomendasi Jurusan**  
       Jurusan dari cluster yang sama akan disarankan sesuai minatmu.
    """)

    # Statistik jurusan dengan nilai tertinggi
    st.markdown("---")
    st.markdown("## 📊 Statistik 3 Jurusan dengan Nilai Rata-rata Tertinggi")

    col_chart_ipa, col_chart_ips = st.columns(2)

    # Grafik untuk jurusan IPA
    with col_chart_ipa:
        st.markdown("#### 📘 IPA")
        df_ipa = load_data("IPA")
        nilai_cols_ipa = ["Matematika", "Bahasa Inggris", "Fisika", "Biologi", "Kimia"]
        rata_ipa = df_ipa.groupby("Jurusan")[nilai_cols_ipa].mean()
        top3_ipa = rata_ipa.mean(axis=1).sort_values(ascending=False).head(3)
        st.bar_chart(top3_ipa)

    # Grafik untuk jurusan IPS
    with col_chart_ips:
        st.markdown("#### 📙 IPS")
        df_ips = load_data("IPS")
        nilai_cols_ips = ["Matematika", "Bahasa Inggris", "Ekonomi", "Geografi", "Sosiologi", "Sejarah"]
        rata_ips = df_ips.groupby("Jurusan")[nilai_cols_ips].mean()
        top3_ips = rata_ips.mean(axis=1).sort_values(ascending=False).head(3)
        st.bar_chart(top3_ips)

# ====================== KOLOM KANAN: FORM INPUT ======================
with col2:
    st.markdown("## 🧾 Form Input")

    # Dropdown jurusan SMA
    jurusan_sma = st.selectbox("Pilih Jurusan SMA:", ["IPA", "IPS"])
    nilai_input = {}

    # Input nilai pelajaran berdasarkan jurusan SMA
    if jurusan_sma == "IPA":
        st.subheader("📘 Nilai Pelajaran IPA")
        nilai_input["Matematika"] = st.slider("Matematika", 0, 100, 75)
        nilai_input["Bahasa Inggris"] = st.slider("Bahasa Inggris", 0, 100, 75)
        nilai_input["Fisika"] = st.slider("Fisika", 0, 100, 75)
        nilai_input["Biologi"] = st.slider("Biologi", 0, 100, 75)
        nilai_input["Kimia"] = st.slider("Kimia", 0, 100, 75)
        fitur = ["Matematika", "Bahasa Inggris", "Fisika", "Biologi", "Kimia"]
    else:
        st.subheader("📙 Nilai Pelajaran IPS")
        nilai_input["Matematika"] = st.slider("Matematika", 0, 100, 75)
        nilai_input["Bahasa Inggris"] = st.slider("Bahasa Inggris", 0, 100, 75)
        nilai_input["Ekonomi"] = st.slider("Ekonomi", 0, 100, 75)
        nilai_input["Geografi"] = st.slider("Geografi", 0, 100, 75)
        nilai_input["Sosiologi"] = st.slider("Sosiologi", 0, 100, 75)
        nilai_input["Sejarah"] = st.slider("Sejarah", 0, 100, 75)
        fitur = ["Matematika", "Bahasa Inggris", "Ekonomi", "Geografi", "Sosiologi", "Sejarah"]

    # Input minat
    minat = st.selectbox("🎯 Pilih Minat Utama:", ["Hitung", "Bicara", "Gambar"])

    # Tombol untuk mendapatkan hasil
    if st.button("🚀 Dapatkan Rekomendasi"):
        df_clean = load_data(jurusan_sma)
        fitur_data = df_clean[fitur + ["Minat"]].dropna()

     # Validasi jika data kosong
        if fitur_data.empty:
            st.error("❌ Tidak ada data yang sesuai.")
            st.stop()

# ====================== PROSES CLUSTERING ======================
        # One-hot encoding & scaling
        fitur_data_encoded = pd.get_dummies(fitur_data, columns=["Minat"])

        # Normalisasi fitur menggunakan StandardScaler
        scaler = StandardScaler()
        X = scaler.fit_transform(fitur_data_encoded)

        # KMeans clustering dengan 3 cluster
        model = KMeans(n_clusters=3, random_state=42, n_init="auto")
        model.fit(X)

        # Simpan hasil cluster ke dalam dataframe
        df_clean["Cluster"] = model.labels_

 # ====================== PREDIKSI CLUSTER USER ======================
        # Membuat dataframe dari input user
        user_df = pd.DataFrame([nilai_input])

        # One-hot encoding minat user
        for m in ["Hitung", "Bicara", "Gambar"]:
            user_df[f"Minat_{m}"] = 1 if minat == m else 0

        # Menyesuaikan kolom user dengan kolom data yang telah diencoding
        for col in fitur_data_encoded.columns:
            if col not in user_df.columns:
                user_df[col] = 0
        user_df = user_df[fitur_data_encoded.columns]

        # Normalisasi data user dan prediksi cluster
        user_X = scaler.transform(user_df)
        cluster_pred = model.predict(user_X)[0]

 # ====================== REKOMENDASI JURUSAN ======================
        # Filter data berdasarkan cluster yang sama
        hasil = df_clean[df_clean["Cluster"] == cluster_pred]

        # Filter lagi berdasarkan minat user
        hasil_minat = hasil[hasil["Minat"].str.lower() == minat.lower()]

        # Jika tidak ada hasil sesuai minat, tampilkan alternatif
        if hasil_minat.empty:
            st.warning("⚠️ Tidak ditemukan jurusan sesuai minat. Menampilkan alternatif terbaik.")
            hasil_minat = hasil

        # Ambil 3 jurusan terpopuler di cluster tersebut
        rekomendasi = hasil_minat["Jurusan"].value_counts().head(3).index.tolist()

        # Tampilkan hasil ke user
        st.success("✅ Rekomendasi Jurusan untuk Kamu:")
        for jur in rekomendasi:
            st.markdown(f"- 🎓 **{jur}**")
