import re

from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

# ==========================================================
# Stopwords
# ==========================================================

factory_stopword = StopWordRemoverFactory()
stop_words = set(factory_stopword.get_stop_words())

custom_stopwords = {
    "lampiran",
    "lampir",
    "halaman",
    "bab",
    "gambar",
    "tabel",
    "nomor",
    "tahun",
    "format",
    "formulir",
    "daftar",
    "isi",
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "nama",
    "depan",
    "belakang",
    "nim",
    "tanda",
    "tangan",
    "cetak",
    "miring",
    "contoh",
    "tanggal",
    "bulan",
    "url",
    "akses",
}

stop_words.update(custom_stopwords)

# ==========================================================
# Stemmer
# ==========================================================

factory_stemmer = StemmerFactory()
stemmer = factory_stemmer.create_stemmer()

# ==========================================================
# Normalization Dictionary
# ==========================================================

NORMALIZATION = {

    "pkmai": "pkm ai",
    "pkmk": "pkm k",
    "pkmkc": "pkm kc",
    "pkmki": "pkm ki",
    "pkmpi": "pkm pi",
    "pkmpm": "pkm pm",
    "pkmrsh": "pkm rsh",
    "pkmgft": "pkm gft",
    "pkmvgk": "pkm vgk",

}

# ==========================================================
# Cleaning
# ==========================================================

def clean_text(text):

    # Gabungkan kata yang terpotong karena hyphen
    text = re.sub(r"(\w)-\s+(\w)", r"\1\2", text)

    # Hapus newline
    text = text.replace("\n", " ")

    # Hapus angka
    text = re.sub(r"\d+", " ", text)

    # Sisakan huruf dan spasi
    text = re.sub(r"[^a-zA-Z\s]", " ", text)

    # Rapikan spasi
    text = re.sub(r"\s+", " ", text)

    return text.strip()

# ==========================================================
# Case Folding
# ==========================================================

def case_folding(text):
    return text.lower()

# ==========================================================
# Normalization
# ==========================================================

def normalize(text):

    for old, new in NORMALIZATION.items():
        text = text.replace(old, new)

    return text

# ==========================================================
# Tokenization
# ==========================================================

def tokenize(text):
    return text.split()

# ==========================================================
# Stopword Removal
# ==========================================================

def remove_stopwords(tokens):

    return [
        token
        for token in tokens
        if token not in stop_words
    ]

# ==========================================================
# Stemming
# ==========================================================

def stemming(tokens):

    return [
        stemmer.stem(token)
        for token in tokens
    ]

# ==========================================================
# Remove Short Token
# ==========================================================

def remove_short_tokens(tokens):

    return [
        token
        for token in tokens
        if len(token) > 1
    ]

# ==========================================================
# Main Pipeline
# ==========================================================

def preprocess_text(text):

    text = clean_text(text)

    text = case_folding(text)

    text = normalize(text)

    tokens = tokenize(text)

    tokens = remove_stopwords(tokens)

    tokens = stemming(tokens)

    tokens = remove_short_tokens(tokens)

    return tokens