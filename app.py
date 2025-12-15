# ======================================
# SURVEY ANALYZER – FINAL (DOSEN READY)
# Descriptive + Correlation Analysis
# ======================================

import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# --------------------------------------
# PAGE CONFIG
# --------------------------------------
st.set_page_config(
    page_title="Survey Analyzer",
    page_icon="📊",
    layout="wide"
)

# --------------------------------------
# CSS STYLE
# --------------------------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #FF97B5, #6E2A85);
    font-family: 'Segoe UI', sans-serif;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #8E4B8E, #6A2C91);
}

.header {
    padding: 40px;
    border-radius: 26px;
    background: linear-gradient(135deg, #FF97B5, #6E2A85);
    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    margin-bottom: 20px;
}

.header h1 {
    color: white;
    font-size: 44px;
    text-shadow: 0 0 14px rgba(255,255,255,0.6);
}

.header p {
    color: #FDEAF3;
    font-size: 18px;
}

.card {
    background: white;
    padding: 26px;
    border-radius: 22px;
    margin-top: 20px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.25);
}

.stButton button {
    background: linear-gradient(135deg, #FF6F91, #845EC2);
    color: white;
    font-weight: bold;
    border-radius: 14px;
    padding: 10px 20px;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------
# LANGUAGE DICTIONARY
# --------------------------------------
LANG = {
    "English": {
        "home": "Home",
        "analyzer": "Survey Analyzer",
        "desc": "Analyze survey data using descriptive statistics and correlation analysis.",
        "upload": "Upload CSV or Excel file",
        "preview": "Data Preview",
        "desc_stat": "Descriptive Statistics",
        "freq": "Frequency & Percentage Table",
        "hist": "Histogram",
        "box": "Boxplot",
        "corr": "Correlation Analysis",
        "select_x": "Select X Variable",
        "select_y": "Select Y Variable",
        "method": "Correlation Method",
        "run": "Run Analysis",
        "result": "Result",
        "interp": "Interpretation"
    },
    "Indonesia": {
        "home": "Beranda",
        "analyzer": "Analisis Survei",
        "desc": "Menganalisis data survei menggunakan statistik deskriptif dan analisis korelasi.",
        "upload": "Unggah file CSV atau Excel",
        "preview": "Pratinjau Data",
        "desc_stat": "Statistik Deskriptif",
        "freq": "Tabel Frekuensi & Persentase",
        "hist": "Histogram",
        "box": "Boxplot",
        "corr": "Analisis Korelasi",
        "select_x": "Pilih Variabel X",
        "select_y": "Pilih Variabel Y",
        "method": "Metode Korelasi",
        "run": "Jalankan Analisis",
        "result": "Hasil",
        "interp": "Interpretasi"
    }
}

# --------------------------------------
# SIDEBAR
# --------------------------------------
with st.sidebar:
    language = st.selectbox("🌐 Language / Bahasa", ["English", "Indonesia"])
    page = st.radio(
        "Navigation",
        [LANG[language]["home"], LANG[language]["analyzer"]],
        label_visibility="collapsed"
    )

T = LANG[language]

# --------------------------------------
# HOME PAGE
# --------------------------------------
if page == T["home"]:
    st.markdown(f"""
    <div class="header">
        <h1>📊 Survey Analyzer</h1>
        <p>{T["desc"]}</p>
    </div>
    """, unsafe_allow_html=True)

# --------------------------------------
# ANALYZER PAGE
# --------------------------------------
else:
    st.markdown(f"""
    <div class="header">
        <h1>📊 {T["analyzer"]}</h1>
        <p>{T["desc"]}</p>
    </div>
    """, unsafe_allow_html=True)

    uploaded = st.file_uploader(T["upload"], type=["csv", "xlsx", "xls"])

    if uploaded:
        # ======================
        # LOAD DATA
        # ======================
        df = pd.read_excel(uploaded) if uploaded.name.endswith(("xlsx", "xls")) else pd.read_csv(uploaded)
        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

        # ======================
        # DATA PREVIEW
        # ======================
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader(T["preview"])
        st.dataframe(df.head())
        st.markdown('</div>', unsafe_allow_html=True)

        # ======================
        # DESCRIPTIVE STATISTICS
        # ======================
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader(T["desc_stat"])

        desc = pd.DataFrame({
            "Mean / Rata-rata": df[numeric_cols].mean(),
            "Median": df[numeric_cols].median(),
            "Mode": df[numeric_cols].mode().iloc[0],
            "Minimum": df[numeric_cols].min(),
            "Maximum": df[numeric_cols].max(),
            "Std Deviation": df[numeric_cols].std()
        })

        st.dataframe(desc)
        st.markdown('</div>', unsafe_allow_html=True)

        # ======================
        # FREQUENCY TABLE
        # ======================
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader(T["freq"])

        col = st.selectbox("Variable", numeric_cols)
        freq = df[col].value_counts().sort_index()
        percent = df[col].value_counts(normalize=True).sort_index() * 100

        freq_df = pd.DataFrame({
            "Frequency": freq,
            "Percentage (%)": percent.round(2)
        })

        st.dataframe(freq_df)
        st.markdown('</div>', unsafe_allow_html=True)

        # ======================
        # HISTOGRAM & BOXPLOT
        # ======================
        st.markdown('<div class="card">', unsafe_allow_html=True)

        fig, ax = plt.subplots(1, 2, figsize=(10, 4))
        ax[0].hist(df[col], bins=5)
        ax[0].set_title(T["hist"])

        ax[1].boxplot(df[col], vert=False)
        ax[1].set_title(T["box"])

        st.pyplot(fig)
        st.markdown('</div>', unsafe_allow_html=True)

        # ======================
        # CORRELATION ANALYSIS
        # ======================
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader(T["corr"])

        # Filter X and Y variables
        x_vars = [c for c in numeric_cols if c.lower() in ["x1","x2","x3","x4","x5","x_total"]]
        y_vars = [c for c in numeric_cols if c.lower() in ["y1","y2","y3","y4","y5","y_total"]]

        x = st.selectbox(T["select_x"], x_vars)
        y = st.selectbox(T["select_y"], y_vars)
        method = st.selectbox(T["method"], ["Pearson", "Spearman"])

        if st.button(T["run"]):
            if method == "Pearson":
                r, p = stats.pearsonr(df[x], df[y])
            else:
                r, p = stats.spearmanr(df[x], df[y])

            # RESULT
            st.subheader(T["result"])
            st.write(f"**Correlation (r)** : {r:.3f}")
            st.write(f"**p-value** : {p:.4f}")

            # INTERPRETATION
            st.subheader(T["interp"])
            strength = (
                "very weak" if abs(r) < 0.2 else
                "weak" if abs(r) < 0.4 else
                "moderate" if abs(r) < 0.6 else
                "strong" if abs(r) < 0.8 else
                "very strong"
            )

            sig = "significant" if p < 0.05 else "not significant"

            if language == "Indonesia":
                st.write(
                    f"Terdapat **hubungan {strength}** antara **{x}** dan **{y}** "
                    f"dengan nilai p **{sig}** (p = {p:.4f})."
                )
            else:
                st.write(
                    f"There is a **{strength} relationship** between **{x}** and **{y}**, "
                    f"and the result is **{sig}** (p = {p:.4f})."
                )

            # VISUALIZATION
            fig2, ax2 = plt.subplots()
            ax2.scatter(df[x], df[y])
            ax2.set_xlabel(x)
            ax2.set_ylabel(y)
            ax2.set_title("Correlation Scatter Plot")
            st.pyplot(fig2)

        st.markdown('</div>', unsafe_allow_html=True)

