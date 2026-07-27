import sys
from pathlib import Path

import streamlit as st

# ==========================================================
# Import Modules
# ==========================================================

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from recommendation import recommend_scheme

# ==========================================================
# Konfigurasi Halaman
# ==========================================================

st.set_page_config(
    page_title="Rekomendasi Skema PKM",
    page_icon="📋",
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

st.title("Rekomendasi Skema PKM")

st.caption(
    "Temukan skema PKM yang paling sesuai berdasarkan karakteristik proyek Anda."
)

st.divider()

# ==========================================================
# Form Input
# ==========================================================

with st.container(border=True):

    st.subheader("Informasi Proyek")

    interest = st.selectbox(
        "Bidang Minat",
        [
            "Artificial Intelligence",
            "Health",
            "Education",
            "Agriculture",
            "Environment",
            "Business",
            "Technology",
            "Social",
            "Creative Industry",
            "Other",
        ]
    )

    objective = st.selectbox(
        "Tujuan Proyek",
        [
            "Research",
            "Entrepreneurship",
            "Community Service",
            "Technology Development",
            "Scientific Writing",
            "Future Ideas",
        ]
    )

    output = st.selectbox(
        "Luaran yang Diharapkan",
        [
            "Research Findings",
            "Prototype",
            "Business Product",
            "Scientific Article",
            "Community Empowerment",
            "Innovation",
        ]
    )

    submit = st.button(
        "Dapatkan Rekomendasi",
        use_container_width=True
    )

# ==========================================================
# Hasil Rekomendasi
# ==========================================================

if submit:

    ranking = recommend_scheme(
        interest,
        objective,
        output
    )

    best = ranking[0]

    total_possible = 85

    compatibility = round(
        best[1] / total_possible * 100
    )

    st.divider()

    st.subheader("Hasil Rekomendasi")

    left, right = st.columns([2, 1])

    with left:

        with st.container(border=True):

            st.success(f"Skema yang Direkomendasikan: {best[0]}")

            st.write(
                "Rekomendasi diberikan berdasarkan kombinasi bidang minat, tujuan proyek, dan luaran yang Anda pilih."
            )

            st.markdown("#### Ringkasan")

            st.write(f"**Bidang Minat:** {interest}")
            st.write(f"**Tujuan Proyek:** {objective}")
            st.write(f"**Luaran:** {output}")

    with right:

        with st.container(border=True):

            st.metric(
                "Tingkat Kesesuaian",
                f"{compatibility}%"
            )

            st.progress(
                compatibility / 100
            )

    st.divider()

    st.subheader("Alternatif Skema Lain")

    cols = st.columns(3)

    for i in range(3):

        scheme, score = ranking[i + 1]

        percent = round(
            score / total_possible * 100
        )

        with cols[i]:

            with st.container(border=True):

                st.markdown(f"### {scheme}")

                st.metric(
                    "Kesesuaian",
                    f"{percent}%"
                )

                st.progress(
                    percent / 100
                )