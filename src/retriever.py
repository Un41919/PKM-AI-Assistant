from pathlib import Path
import re

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# ==========================================================
# Embedding
# ==========================================================

embedding_model = HuggingFaceEmbeddings(
    model_name="intfloat/multilingual-e5-base"
)

# ==========================================================
# Vector Database
# ==========================================================

vector_db = Chroma(
    persist_directory="data/vector_db",
    embedding_function=embedding_model
)

# ==========================================================
# Metadata Cleaner
# ==========================================================

def clean_source(source):

    name = Path(source).stem

    name = name.replace("_fix", "")
    name = name.replace("2026", "")
    name = name.replace("_", " ")
    name = name.replace("-", " ")

    name = re.sub(r"\bfix\b", "", name, flags=re.IGNORECASE)
    name = " ".join(name.split())

    mapping = {

        "PKM Panduan Umum": "Panduan Umum",

        "PKM AI": "PKM-AI",
        "PKM K": "PKM-K",
        "PKM KC": "PKM-KC",
        "PKM KI": "PKM-KI",
        "PKM PM": "PKM-PM",
        "PKM PI": "PKM-PI",
        "PKM RE": "PKM-RE",
        "PKM RSH": "PKM-RSH",
        "PKM VGK": "PKM-VGK",
        "PKM GFT": "PKM-GFT"

    }

    return mapping.get(name, name)

# ==========================================================
# Query Router
# ==========================================================

def route_query(query):

    q = query.lower()

    keyword_map = {

        "pkm-ai": "PKM-AI",
        "artikel ilmiah": "PKM-AI",

        "pkm-k": "PKM-K",
        "wirausaha": "PKM-K",
        "kewirausahaan": "PKM-K",
        "usaha": "PKM-K",

        "pkm-kc": "PKM-KC",
        "karsa cipta": "PKM-KC",
        "prototipe": "PKM-KC",

        "pkm-ki": "PKM-KI",
        "karya inovatif": "PKM-KI",

        "pkm-pm": "PKM-PM",
        "pengabdian": "PKM-PM",
        "masyarakat": "PKM-PM",

        "pkm-pi": "PKM-PI",
        "penerapan iptek": "PKM-PI",

        "pkm-re": "PKM-RE",
        "riset eksakta": "PKM-RE",

        "pkm-rsh": "PKM-RSH",
        "riset sosial": "PKM-RSH",

        "pkm-vgk": "PKM-VGK",
        "video": "PKM-VGK",
        "gagasan": "PKM-VGK",

        "pkm-gft": "PKM-GFT",
        "gagasan futuristik": "PKM-GFT"

    }

    for keyword, scheme in keyword_map.items():

        if keyword in q:

            return scheme

    return "GENERAL"

# ==========================================================
# Adaptive Retriever
# ==========================================================

def get_retriever(query):

    query_type = route_query(query)

    if query_type == "GENERAL":

        k = 8
        fetch_k = 25

    else:

        k = 5
        fetch_k = 20

    return vector_db.as_retriever(

        search_type="mmr",

        search_kwargs={

            "k": k,
            "fetch_k": fetch_k,
            "lambda_mult": 0.7

        }

    )

# ==========================================================
# Source Diversity
# ==========================================================

def diversify_results(query, docs):

    query_type = route_query(query)

    selected = []
    used_sources = set()

    # ------------------------------------------------------
    # Pertanyaan umum:
    # Prioritaskan satu chunk terbaik dari Panduan Umum
    # ------------------------------------------------------

    if query_type == "GENERAL":

        for doc in docs:

            source = clean_source(doc.metadata["source"])

            if source == "Panduan Umum":

                selected.append(doc)
                used_sources.add(source)
                break

    # ------------------------------------------------------
    # Ambil satu chunk terbaik dari setiap source
    # ------------------------------------------------------

    for doc in docs:

        source = clean_source(doc.metadata["source"])

        if source in used_sources:
            continue

        selected.append(doc)
        used_sources.add(source)

        if len(selected) >= 5:
            return selected

    # ------------------------------------------------------
    # Jika masih kurang dari 5,
    # isi dengan chunk berikutnya
    # ------------------------------------------------------

    if len(selected) < 5:

        for doc in docs:

            if doc in selected:
                continue

            selected.append(doc)

            if len(selected) >= 5:
                break

    return selected

# ==========================================================
# Query Expansion
# ==========================================================

def expand_query(query):

    q = query.lower()

    additions = []

    if "jumlah anggota" in q:
        additions.extend([
            "tim",
            "peserta",
            "kriteria pengusulan"
        ])

    if "ketua" in q:
        additions.extend([
            "tim",
            "anggota",
            "pengusul"
        ])

    if "syarat" in q:
        additions.extend([
            "kriteria",
            "pengusulan",
            "persyaratan"
        ])

    if "luaran" in q:
        additions.extend([
            "luaran wajib",
            "output"
        ])

    if "tujuan" in q:
        additions.append("objective")

    if additions:
        query = query + " " + " ".join(additions)

    return query

# ==========================================================
# Search
# ==========================================================

def search(query):

    expanded_query = expand_query(query)

    query_type = route_query(query)

    # =====================================================
    # Query Umum
    # =====================================================

    if query_type == "GENERAL":

        docs = vector_db.max_marginal_relevance_search(
            expanded_query,
            k=5,
            fetch_k=20,
            lambda_mult=0.7
        )

        docs = diversify_results(query, docs)

        return docs

    # =====================================================
    # Query Khusus PKM
    # =====================================================

    mapping = {

        "PKM-AI": "PKM-AI-2026_fix.pdf",
        "PKM-K": "PKM-K-2026_fix.pdf",
        "PKM-KC": "PKM-KC 2026 fix.pdf",
        "PKM-KI": "PKM-KI-2026_fix.pdf",
        "PKM-PM": "PKM-PM-2026_fix.pdf",
        "PKM-PI": "PKM-PI-2026_fix.pdf",
        "PKM-RE": "PKM-RE-2026_fix.pdf",
        "PKM-RSH": "PKM-RSH-2026_fix.pdf",
        "PKM-VGK": "PKM-VGK-2026_fix.pdf",
        "PKM-GFT": "PKM-GFT-2026_fix.pdf"

    }

    filename = mapping[query_type]

    docs = vector_db.similarity_search(

        expanded_query,

        k=8,

        filter={

            "source": f"data\\raw\\{filename}"

        }

    )

    return docs


# ==========================================================
# Pretty Print
# ==========================================================

def show(query):

    docs = search(query)

    print("=" * 90)
    print("QUERY")
    print("=" * 90)
    print(query)

    print("\nQuery Type :", route_query(query))

    print("\n" + "=" * 90)
    print(f"Retrieved Documents : {len(docs)}")
    print("=" * 90)

    for i, doc in enumerate(docs):

        source = clean_source(
            doc.metadata["source"]
        )

        page = doc.metadata.get("page", 0) + 1

        print()

        print("=" * 90)
        print(f"RESULT {i+1}")
        print("=" * 90)

        print(doc.metadata)
        print(f"Source : {source}")
        print(f"Page   : {page}")

        print("-" * 90)

        print(doc.page_content[:700])

        print()

# ==========================================================
# Metadata Filter
# ==========================================================

def get_source_filter(query):

    query_type = route_query(query)

    if query_type == "GENERAL":
        return None

    mapping = {
        "PKM-AI": "PKM-AI",
        "PKM-K": "PKM-K-",
        "PKM-KC": "PKM-KC",
        "PKM-KI": "PKM-KI",
        "PKM-PM": "PKM-PM",
        "PKM-PI": "PKM-PI",
        "PKM-RE": "PKM-RE",
        "PKM-RSH": "PKM-RSH",
        "PKM-VGK": "PKM-VGK",
        "PKM-GFT": "PKM-GFT"
    }

    return mapping.get(query_type)

# ==========================================================
# Return Context for RAG
# ==========================================================

def retrieve_context(query):

    docs = search(query)

    context = []

    seen = set()

    for doc in docs:

        source = clean_source(doc.metadata["source"])

        page = doc.metadata.get("page", 0) + 1

        key = (source, page)

        # Skip jika halaman sudah pernah dimasukkan
        if key in seen:
            continue

        seen.add(key)

        text = f"""
[Sumber: {source} | Halaman {page}]

{doc.page_content}
"""

        context.append(text)

    return "\n\n" + ("-" * 80 + "\n\n").join(context)


# ==========================================================
# Return Documents
# ==========================================================

def retrieve_documents(query):

    return search(query)


# ==========================================================
# Main
# ==========================================================

if __name__ == "__main__":

    print("=" * 90)
    print("PKM AI Assistant - Retriever v2.6")
    print("Type 'exit' to quit")
    print("=" * 90)

    while True:

        query = input("\nQuestion : ")

        if query.lower() == "exit":
            break

        print()

        show(query)