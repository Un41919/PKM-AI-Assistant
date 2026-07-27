from pathlib import Path

import pandas as pd

from rag_pipeline import load_documents
from preprocessing import preprocess_text

# Folder output
OUTPUT_DIR = Path("data/processed")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def process_documents():

    print("=" * 80)
    print("Loading Documents...")
    print("=" * 80)

    documents = load_documents()

    rows = []

    for doc in documents:

        raw_text = doc.page_content

        # Skip halaman kosong (cover)
        if not raw_text.strip():
            continue

        # Skip halaman daftar isi
        if "DAFTAR ISI" in raw_text.upper():
            continue

        tokens = preprocess_text(raw_text)

        processed_text = " ".join(tokens)

        rows.append({
            "Source": Path(doc.metadata["source"]).name,
            "Page": doc.metadata["page"] + 1,
            "Raw Text": raw_text,
            "Processed Text": processed_text,
            "Tokens": ", ".join(tokens)
        })

    df = pd.DataFrame(rows)

    output_file = OUTPUT_DIR / "processed_documents.xlsx"

    df.to_excel(output_file, index=False)

    print("\nProcessing Finished!")
    print(f"Total Documents : {len(df)}")
    print(f"Saved to : {output_file}")


if __name__ == "__main__":
    process_documents()