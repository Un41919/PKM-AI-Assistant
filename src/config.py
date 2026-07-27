from pathlib import Path

# ==============================
# Directories
# ==============================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

VECTOR_DB_DIR = PROJECT_ROOT / "data" / "vector_db"

# ==============================
# Chunking
# ==============================

CHUNK_SIZE = 800

CHUNK_OVERLAP = 150

# ==============================
# Embedding Model
# ==============================

EMBEDDING_MODEL = "intfloat/multilingual-e5-base"