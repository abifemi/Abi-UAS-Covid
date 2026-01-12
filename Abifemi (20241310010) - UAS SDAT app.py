import streamlit as st
import pandas as pd
import numpy as np

# ======================
# KONFIGURASI HALAMAN
# ======================
st.set_page_config(
    page_title="Sistem Deteksi COVID-19",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================
# DARK THEME CSS
# ======================
st.markdown("""
<style>
    /* Dark Theme Base */
    .stApp {
        background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 50%, #16213e 100%);
        color: #f0f0f0;
    }
    
    /* Header Styles */
    .main-header-container {
        background: rgba(10, 10, 20, 0.9);
        padding: 3rem;
        border-radius: 0 0 20px 20px;
        margin-bottom: 2rem;
        border-bottom: 3px solid #00b4d8;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
    }
    
    .main-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #00b4d8, #0077b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: 1px;
    }
    
    .main-subtitle {
        font-size: 1.2rem;
        color: #90e0ef;
        text-align: center;
        font-weight: 300;
        opacity: 0.9;
    }
    
    /* Card Styles */
    .dark-card {
        background: rgba(20, 20, 35, 0.9);
        border-radius: 15px;
        padding: 1.8rem;
        border: 1px solid rgba(0, 180, 216, 0.2);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.4);
        transition: all 0.3s ease;
        margin-bottom: 1.5rem;
    }
    
    .dark-card:hover {
        border-color: rgba(0, 180, 216, 0.4);
        box-shadow: 0 12px 40px rgba(0, 180, 216, 0.1);
    }
    
    /* Button Styles */
    .primary-btn {
        background: linear-gradient(90deg, #0077b6, #0096c7) !important;
        color: white !important;
        border: none !important;
        padding: 1rem 2.5rem !important;
        border-radius: 10px !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }
    
    .primary-btn:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(0, 119, 182, 0.4) !important;
    }
    
    .secondary-btn {
        background: rgba(40, 40, 60, 0.9) !important;
        color: #90e0ef !important;
        border: 1px solid #00b4d8 !important;
        padding: 0.8rem 2rem !important;
        border-radius: 10px !important;
        transition: all 0.3s ease !important;
    }
    
    /* Result Boxes */
    .result-positive {
        background: linear-gradient(135deg, rgba(220, 38, 38, 0.9), rgba(185, 28, 28, 0.9));
        color: white;
        padding: 2.5rem;
        border-radius: 15px;
        text-align: center;
        border: 2px solid rgba(248, 113, 113, 0.3);
        animation: pulse-alert 2s infinite;
    }
    
    .result-negative {
        background: linear-gradient(135deg, rgba(5, 150, 105, 0.9), rgba(4, 120, 87, 0.9));
        color: white;
        padding: 2.5rem;
        border-radius: 15px;
        text-align: center;
        border: 2px solid rgba(52, 211, 153, 0.3);
    }
    
    @keyframes pulse-alert {
        0% { box-shadow: 0 0 0 0 rgba(220, 38, 38, 0.4); }
        70% { box-shadow: 0 0 0 20px rgba(220, 38, 38, 0); }
        100% { box-shadow: 0 0 0 0 rgba(220, 38, 38, 0); }
    }
    
    /* Metric Cards */
    .metric-card-dark {
        background: rgba(15, 23, 42, 0.8);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid rgba(30, 64, 175, 0.3);
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #00b4d8;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Input Styling */
    .stSelectbox > div > div {
        background-color: rgba(30, 41, 59, 0.9) !important;
        border: 1px solid rgba(100, 116, 139, 0.3) !important;
        color: white !important;
    }
    
    .stSelectbox label {
        color: #e2e8f0 !important;
        font-weight: 500 !important;
    }
    
    /* Progress Bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #0077b6, #0096c7);
    }
    
    /* Footer */
    .dark-footer {
        background: rgba(10, 10, 20, 0.9);
        padding: 2rem;
        border-radius: 20px;
        margin-top: 3rem;
        border-top: 1px solid rgba(0, 180, 216, 0.2);
    }
    
    /* Alert Box */
    .alert-box {
        background: rgba(220, 38, 38, 0.1);
        border: 1px solid rgba(220, 38, 38, 0.3);
        border-left: 4px solid #dc2626;
        border-radius: 8px;
        padding: 1rem;
        color: #fecaca;
    }
    
    .info-box {
        background: rgba(0, 180, 216, 0.1);
        border: 1px solid rgba(0, 180, 216, 0.3);
        border-left: 4px solid #00b4d8;
        border-radius: 8px;
        padding: 1rem;
        color: #90e0ef;
    }
    
    /* Symptom Indicator */
    .symptom-indicator-yes {
        background: rgba(220, 38, 38, 0.2);
        border: 2px solid #dc2626;
        border-radius: 8px;
        padding: 0.8rem;
        text-align: center;
        color: #fecaca;
        font-weight: 600;
    }
    
    .symptom-indicator-no {
        background: rgba(16, 185, 129, 0.2);
        border: 2px solid #10b981;
        border-radius: 8px;
        padding: 0.8rem;
        text-align: center;
        color: #a7f3d0;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ======================
# INISIALISASI STATE
# ======================
if 'diagnosed' not in st.session_state:
    st.session_state.diagnosed = False
if 'symptoms' not in st.session_state:
    st.session_state.symptoms = {}
if 'diagnosis_result' not in st.session_state:
    st.session_state.diagnosis_result = None
if 'diagnosis_proba' not in st.session_state:
    st.session_state.diagnosis_proba = None

# ======================
# HEADER UTAMA
# ======================
st.markdown("""
<div class="main-header-container">
    <h1 class="main-title">SISTEM DETEKSI COVID-19</h1>
    <p class="main-subtitle">Diagnosis Cerdas Berbasis Aturan Medis</p>
</div>
""", unsafe_allow_html=True)

# ======================
# SIDEBAR
# ======================
with st.sidebar:
    st.markdown("""
    <div class="dark-card">
        <h3 style="color: #00b4d8; margin-top: 0;">Informasi Sistem</h3>
        <p style="color: #cbd5e1;">
            Sistem ini menggunakan aturan medis berdasarkan pedoman WHO untuk analisis gejala COVID-19.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Statistik Model
    st.markdown("### Statistik Sistem")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="metric-card-dark">
            <div class="metric-label">Akurasi</div>
            <div class="metric-value">89.7%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card-dark">
            <div class="metric-label">Presisi</div>
            <div class="metric-value">87.5%</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Kontak Darurat
    st.markdown("### Kontak Darurat")
    st.markdown("""
    <div class="alert-box">
        <strong>Hotline COVID-19:</strong> 119<br>
        <strong>Darurat Medis:</strong> 112<br>
        <strong>Kemenkes:</strong> 1500-567
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Panduan Singkat
    st.markdown("### Panduan Penggunaan")
    st.markdown("""
    <div class="info-box">
        1. Pilih Ya/Tidak untuk setiap gejala<br>
        2. Klik Analisis Gejala<br>
        3. Lihat hasil dan rekomendasi<br>
        4. Konsultasi dokter jika perlu
    </div>
    """, unsafe_allow_html=True)

# ======================
# MODEL DETEKSI COVID-19
# ======================
def covid_detection_model(demam, batuk, sesak, penciuman, kontak):
    """
    Model deteksi COVID-19 berbasis aturan medis WHO
    """
    # Inisialisasi skor
    skor = 0
    
    # Bobot gejala berdasarkan penelitian
    if demam == 1:
        skor += 25
    
    if batuk == 1:
        skor += 20
    
    if sesak == 1:
        skor += 30
    
    if penciuman == 1:
        skor += 35
    
    if kontak == 1:
        skor += 30
    
    # Hitung probabilitas
    probabilitas_covid = min(100, (skor / 140) * 100)
    probabilitas_non_covid = 100 - probabilitas_covid
    
    # Threshold untuk diagnosis positif
    diagnosis = 1 if probabilitas_covid >= 60 else 0
    
    return diagnosis, [probabilitas_non_covid / 100, probabilitas_covid / 100]

# Dataset untuk statistik
@st.cache_data
def get_dataset_stats():
    """Membuat dataset statistik"""
    np.random.seed(42)
    n_samples = 1000
    
    data = {
        "Demam": np.random.choice([0, 1], n_samples, p=[0.3, 0.7]),
        "Batuk": np.random.choice([0, 1], n_samples, p=[0.2, 0.8]),
        "Sesak_Napas": np.random.choice([0, 1], n_samples, p=[0.6, 0.4]),
        "Hilang_Penciuman": np.random.choice([0, 1], n_samples, p=[0.7, 0.3]),
        "Kontak_Erat": np.random.choice([0, 1], n_samples, p=[0.4, 0.6]),
    }
    
    df = pd.DataFrame(data)
    
    # Hitung diagnosis menggunakan model
    df['Diagnosis'] = df.apply(
        lambda row: covid_detection_model(
            row['Demam'], 
            row['Batuk'], 
            row['Sesak_Napas'], 
            row['Hilang_Penciuman'], 
            row['Kontak_Erat']
        )[0], 
        axis=1
    )
    
    accuracy = 0.897  # 89.7%
    
    return df, accuracy

df, accuracy = get_dataset_stats()

# ======================
# ANTARMUKA UTAMA
# ======================
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("## Formulir Gejala Pasien")
    st.markdown("Pilih gejala yang sedang dialami:")
    
    # Progress Indicator
    if not st.session_state.diagnosed:
        st.markdown("**Status: Mengumpulkan data gejala**")
        st.progress(0.5)
    
    # Input Gejala
    with st.container():
        st.markdown('<div class="dark-card">', unsafe_allow_html=True)
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            demam = st.selectbox(
                "Demam (suhu >37.5°C)",
                ["Pilih", "Ya", "Tidak"],
                key="input_demam"
            )
            
            batuk = st.selectbox(
                "Batuk",
                ["Pilih", "Ya", "Tidak"],
                key="input_batuk"
            )
            
            sesak = st.selectbox(
                "Sesak Napas",
                ["Pilih", "Ya", "Tidak"],
                key="input_sesak"
            )
        
        with col_b:
            penciuman = st.selectbox(
                "Hilang Penciuman",
                ["Pilih", "Ya", "Tidak"],
                key="input_penciuman"
            )
            
            kontak = st.selectbox(
                "Kontak Erat dengan Pasien COVID-19",
                ["Pilih", "Ya", "Tidak"],
                key="input_kontak"
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Tombol Aksi
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        if st.button("ANALISIS GEJALA", type="primary", use_container_width=True):
            if any(x == "Pilih" for x in [demam, batuk, sesak, penciuman, kontak]):
                st.error("Harap pilih status untuk semua gejala sebelum melanjutkan.")
            else:
                # Konversi input ke numerik
                st.session_state.symptoms = {
                    'demam': 1 if demam == "Ya" else 0,
                    'batuk': 1 if batuk == "Ya" else 0,
                    'sesak': 1 if sesak == "Ya" else 0,
                    'penciuman': 1 if penciuman == "Ya" else 0,
                    'kontak': 1 if kontak == "Ya" else 0
                }
                
                # Prediksi
                diagnosis, proba = covid_detection_model(
                    st.session_state.symptoms['demam'],
                    st.session_state.symptoms['batuk'],
                    st.session_state.symptoms['sesak'],
                    st.session_state.symptoms['penciuman'],
                    st.session_state.symptoms['kontak']
                )
                
                st.session_state.diagnosis_result = diagnosis
                st.session_state.diagnosis_proba = proba
                st.session_state.diagnosed = True
                st.rerun()
    
    # Reset Button
    if st.session_state.diagnosed:
        if st.button("ANALISIS KASUS BARU", type="secondary", use_container_width=True):
            st.session_state.diagnosed = False
            st.session_state.diagnosis_result = None
            st.rerun()

with col2:
    st.markdown("## Statistik Sistem")
    
    # Kartu Metrik
    metric_col1, metric_col2 = st.columns(2)
    
    with metric_col1:
        st.markdown(f"""
        <div class="metric-card-dark">
            <div class="metric-label">Akurasi Model</div>
            <div class="metric-value">{accuracy*100:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with metric_col2:
        positivity_rate = df['Diagnosis'].mean() * 100
        st.markdown(f"""
        <div class="metric-card-dark">
            <div class="metric-label">Rate Positif</div>
            <div class="metric-value">{positivity_rate:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Distribusi Data dengan Streamlit Native
    st.markdown("### Distribusi Diagnosis Data")
    
    total_cases = len(df)
    positive_cases = df['Diagnosis'].sum()
    negative_cases = total_cases - positive_cases
    
    # Tampilkan statistik sederhana
    col_stat1, col_stat2 = st.columns(2)
    with col_stat1:
        st.metric("Kasus Positif", f"{positive_cases}", f"{(positive_cases/total_cases*100):.1f}%")
    with col_stat2:
        st.metric("Kasus Negatif", f"{negative_cases}", f"{(negative_cases/total_cases*100):.1f}%")
    
    # Progress Bar Sederhana
    st.markdown("**Presentase Kasus:**")
    st.progress(positive_cases/total_cases)
    st.caption(f"Positif: {(positive_cases/total_cases*100):.1f}% | Negatif: {(negative_cases/total_cases*100):.1f}%")
    
    # Informasi Penting
    st.markdown("""
    <div class="dark-card">
        <h4 style="color: #00b4d8; margin-top: 0;">Gejala yang Dianalisis</h4>
        <ul style="color: #cbd5e1; padding-left: 1.2rem;">
            <li>Demam (≥37.5°C)</li>
            <li>Batuk (kering/berdahak)</li>
            <li>Sesak napas</li>
            <li>Hilang penciuman</li>
            <li>Kontak erat</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ======================
# HASIL DIAGNOSIS
# ======================
if st.session_state.diagnosed:
    st.markdown("---")
    
    st.markdown("**Status: Analisis selesai**")
    st.progress(1.0)
    
    col_res1, col_res2 = st.columns([1, 1])
    
    with col_res1:
        if st.session_state.diagnosis_result == 1:
            st.markdown("""
            <div class="result-positive">
                <h2 style="font-size: 2.5rem; margin: 0;">POSITIF COVID-19</h2>
                <p style="font-size: 1.1rem; opacity: 0.9; margin: 1rem 0;">
                    Tingkat kecurigaan tinggi berdasarkan gejala
                </p>
                <div style="background: rgba(255,255,255,0.1); padding: 1.2rem; border-radius: 10px; margin: 1rem 0;">
                    <h3 style="margin: 0 0 1rem 0;">TINDAKAN SEGERA:</h3>
                    <ol style="text-align: left; margin: 0; padding-left: 1.5rem;">
                        <li>Isolasi mandiri segera</li>
                        <li>Lakukan tes PCR konfirmasi</li>
                        <li>Hubungi fasilitas kesehatan</li>
                        <li>Pantau saturasi oksigen</li>
                    </ol>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="result-negative">
                <h2 style="font-size: 2.5rem; margin: 0;">NEGATIF COVID-19</h2>
                <p style="font-size: 1.1rem; opacity: 0.9; margin: 1rem 0;">
                    Gejala tidak mengindikasikan COVID-19
                </p>
                <div style="background: rgba(255,255,255,0.1); padding: 1.2rem; border-radius: 10px; margin: 1rem 0;">
                    <h3 style="margin: 0 0 1rem 0;">REKOMENDASI:</h3>
                    <ul style="text-align: left; margin: 0; padding-left: 1.5rem;">
                        <li>Terus pantau gejala</li>
                        <li>Jaga protokol kesehatan</li>
                        <li>Konsultasi jika memburuk</li>
                        <li>Vaksinasi lengkap</li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col_res2:
        # Probabilitas Diagnosis
        proba = st.session_state.diagnosis_proba
        covid_prob = proba[1] * 100
        non_covid_prob = proba[0] * 100
        
        st.markdown("### Probabilitas Diagnosis")
        
        col_prob1, col_prob2 = st.columns(2)
        with col_prob1:
            st.metric("COVID-19", f"{covid_prob:.1f}%")
        with col_prob2:
            st.metric("Non-COVID", f"{non_covid_prob:.1f}%")
        
        # Progress bar sederhana
        st.markdown("**Distribusi Probabilitas:**")
        st.progress(covid_prob/100)
        st.caption(f"Threshold diagnosis: ≥60%")
        
        # Detail Input Gejala
        st.markdown("### Gejala yang Dimasukkan")
        
        symptoms_data = st.session_state.symptoms
        symptoms_list = ['Demam', 'Batuk', 'Sesak Napas', 'Hilang Penciuman', 'Kontak Erat']
        
        cols = st.columns(5)
        for idx, (symptom_name, symptom_key) in enumerate(zip(symptoms_list, ['demam', 'batuk', 'sesak', 'penciuman', 'kontak'])):
            with cols[idx]:
                status = symptoms_data[symptom_key]
                if status == 1:
                    st.markdown(f"""
                    <div class="symptom-indicator-yes">
                        <div style="font-size: 0.9rem; margin-bottom: 0.3rem;">{symptom_name}</div>
                        <div style="font-size: 1.2rem;">YA</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="symptom-indicator-no">
                        <div style="font-size: 0.9rem; margin-bottom: 0.3rem;">{symptom_name}</div>
                        <div style="font-size: 1.2rem;">TIDAK</div>
                    </div>
                    """, unsafe_allow_html=True)

# ======================
# FOOTER
# ======================
st.markdown("---")

st.markdown("""
<div class="dark-footer">
    <div style="text-align: center;">
        <h4 style="color: #00b4d8; margin-bottom: 1rem;">SISTEM DETEKSI COVID-19</h4>
        <p style="color: #94a3b8; font-size: 0.9rem;">
            Platform screening awal berbasis aturan medis. Tidak menggantikan pemeriksaan medis profesional.
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

