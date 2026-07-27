import sys
from pathlib import Path

import streamlit as st

# ==========================================================
# Import Modules
# ==========================================================

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from retriever import retrieve_context
from llm import generate_answer

# ==========================================================
# Konfigurasi Halaman
# ==========================================================

st.set_page_config(
    page_title="Tanya PKM",
    page_icon="💬",
    layout="wide"
)

# ==========================================================
# Sidebar
# ==========================================================

with st.sidebar:

    st.title("PKM AI Assistant")

    st.divider()

    if st.button(
        "Hapus Percakapan",
        use_container_width=True
    ):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.markdown("### Informasi Aplikasi")

    st.write("**Versi:** 1.0")

    st.write("**Dataset:** Panduan PKM 2026")

# ==========================================================
# Header
# ==========================================================

st.title("Tanya PKM")

st.caption(
    "Ajukan pertanyaan mengenai Panduan Program Kreativitas Mahasiswa (PKM) Tahun 2026."
)

st.divider()

# ==========================================================
# Inisialisasi Riwayat Percakapan
# ==========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# ==========================================================
# Tampilan Awal
# ==========================================================

if len(st.session_state.messages) == 0:

    with st.container(border=True):

        st.subheader("Mulai Percakapan")

        st.write(
            """
Ajukan pertanyaan mengenai **Panduan Program Kreativitas Mahasiswa (PKM) Tahun 2026** menggunakan bahasa alami.

Sistem akan menelusuri dokumen panduan resmi PKM dan menghasilkan jawaban berdasarkan informasi yang ditemukan, disertai sumber referensinya.
"""
        )

# ==========================================================
# Tampilkan Riwayat Percakapan
# ==========================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# ==========================================================
# Input Pertanyaan
# ==========================================================

question = st.chat_input(
    "Ketik pertanyaan Anda di sini..."
)

# ==========================================================
# Proses Pertanyaan
# ==========================================================

if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):

        st.markdown(question)

    with st.spinner("Mencari jawaban pada Panduan PKM..."):

        context = retrieve_context(question)

        answer = generate_answer(
            question,
            context
        )

    # ======================================================
    # Ambil Sumber
    # ======================================================

    citation = ""

    try:

        first = context.split("-" * 80)[0]

        for line in first.split("\n"):

            if line.startswith("[Sumber:"):

                citation = (
                    line.replace("[", "")
                        .replace("]", "")
                        .strip()
                )

                break

    except Exception:

        citation = ""

    # ======================================================
    # Tampilkan Jawaban
    # ======================================================

    with st.chat_message("assistant"):

        st.markdown(answer)

        if citation:

            st.caption(f"Sumber: {citation}")

    # ======================================================
    # Simpan Riwayat
    # ======================================================

    history = answer

    if citation:

        history += f"\n\n*Sumber: {citation}*"

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": history
        }
    )