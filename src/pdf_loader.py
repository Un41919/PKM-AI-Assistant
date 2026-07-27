from pathlib import Path
from pypdf import PdfReader

# ==========================================================
# Configuration
# ==========================================================

RAW_DATA_DIR = Path("data/raw")

# ==========================================================
# Load First PDF
# ==========================================================

pdf_file = next(RAW_DATA_DIR.glob("*.pdf"))

print(f"\nMembaca file : {pdf_file.name}")

reader = PdfReader(pdf_file)

print(f"Jumlah halaman : {len(reader.pages)}")

# ==========================================================
# Read First 5 Pages
# ==========================================================

for i, page in enumerate(reader.pages[:5], start=1):

    print("\n" + "=" * 80)
    print(f"HALAMAN {i}")
    print("=" * 80)

    text = page.extract_text()

    if text and text.strip():
        print(text[:500])      # tampilkan 500 karakter pertama
    else:
        print("[Tidak ada teks yang berhasil diekstrak]")