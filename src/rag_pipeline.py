from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from text_splitter import create_text_splitter

RAW_DATA_DIR = Path("data/raw")

# ==========================================================
# Halaman yang tidak perlu di-index
# ==========================================================

SKIP_KEYWORDS = [
    "DAFTAR ISI",
    "KATA PENGANTAR"
]


def should_skip(text):

    text = text.upper()

    return any(
        keyword in text
        for keyword in SKIP_KEYWORDS
    )


# ==========================================================
# Load Documents
# ==========================================================

def load_documents():

    documents = []

    pdf_files = sorted(RAW_DATA_DIR.glob("*.pdf"))

    for pdf in pdf_files:

        print(f"Loading {pdf.name}")

        loader = PyPDFLoader(str(pdf))

        docs = loader.load()

        kept = 0
        skipped = 0

        for doc in docs:

            if should_skip(doc.page_content):

                skipped += 1
                continue

            documents.append(doc)
            kept += 1

        print(f"  Kept    : {kept}")
        print(f"  Skipped : {skipped}")

    return documents


# ==========================================================
# Split Documents
# ==========================================================

def split_documents(documents):

    splitter = create_text_splitter()

    chunks = splitter.split_documents(documents)

    return chunks


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    documents = load_documents()

    chunks = split_documents(documents)

    print("\n" + "=" * 80)
    print(f"Total Documents : {len(documents)}")
    print(f"Total Chunks    : {len(chunks)}")
    print("=" * 80)

    print("\nMetadata")
    print(chunks[0].metadata)

    print("\nContent")
    print(chunks[0].page_content)