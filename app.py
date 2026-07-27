import streamlit as st

# ==========================================================
# Konfigurasi Halaman
# ==========================================================

st.set_page_config(
    page_title="PKM AI Assistant",
    page_icon="🎓",
    layout="wide"
)

# ==========================================================
# Sidebar
# ==========================================================

with st.sidebar:

    st.title("PKM AI Assistant")

    st.divider()

    st.markdown("### Informasi Aplikasi")

    st.write("**Versi:** 1.0")

    st.write("**Dataset:** Panduan PKM 2026")

# ==========================================================
# Header
# ==========================================================

st.title("PKM AI Assistant")

st.markdown(
    """
### Asisten Cerdas untuk Panduan Program Kreativitas Mahasiswa (PKM) Tahun 2026

PKM AI Assistant membantu mahasiswa memperoleh informasi dari dokumen resmi Panduan PKM Tahun 2026 serta memberikan rekomendasi skema PKM yang sesuai berdasarkan minat, tujuan proyek, dan luaran yang diharapkan.
"""
)

st.divider()

# ==========================================================
# Fitur
# ==========================================================

st.header("Fitur")

col1, col2 = st.columns(2)

with col1:

    with st.container(border=True):

        st.subheader("Tanya PKM")

        st.write(
            """
Ajukan pertanyaan mengenai Panduan PKM Tahun 2026 menggunakan bahasa alami.

Sistem akan menelusuri dokumen panduan resmi dan menghasilkan jawaban beserta sumber referensinya.
"""
        )

        st.markdown("**Contoh Pertanyaan**")

        st.write("- Apa tujuan PKM-K?")
        st.write("- Apa luaran wajib PKM-AI?")
        st.write("- Berapa jumlah anggota tim PKM?")

with col2:

    with st.container(border=True):

        st.subheader("Rekomendasi Skema PKM")

        st.write(
            """
Temukan skema PKM yang paling sesuai berdasarkan minat, tujuan proyek, dan luaran yang diharapkan.
"""
        )

        st.markdown("**Rekomendasi Berdasarkan**")

        st.write("- Bidang minat")
        st.write("- Tujuan proyek")
        st.write("- Luaran yang diharapkan")

st.divider()

# ==========================================================
# Cara Penggunaan
# ==========================================================

st.header("Cara Penggunaan")

with st.container(border=True):

    st.write("1. Buka halaman **Tanya PKM** untuk mencari informasi mengenai Panduan PKM Tahun 2026.")

    st.write("2. Buka halaman **Rekomendasi Skema PKM** untuk memperoleh rekomendasi skema PKM yang paling sesuai.")

    st.write("3. Baca jawaban beserta sumber referensi yang ditampilkan.")

st.divider()

# ==========================================================
# Dokumen yang Didukung
# ==========================================================

st.header("Dokumen yang Didukung")

docs = [
    "Panduan Umum PKM",
    "PKM-K",
    "PKM-KC",
    "PKM-KI",
    "PKM-RE",
    "PKM-RSH",
    "PKM-PM",
    "PKM-PI",
    "PKM-AI",
    "PKM-VGK",
    "PKM-GFT"
]

col1, col2 = st.columns(2)

half = len(docs) // 2 + len(docs) % 2

with col1:

    with st.container(border=True):

        for doc in docs[:half]:
            st.write(f"• {doc}")

with col2:

    with st.container(border=True):

        for doc in docs[half:]:
            st.write(f"• {doc}")

st.divider()

st.caption("PKM AI Assistant | UAS Analisis Tren dan Topik")