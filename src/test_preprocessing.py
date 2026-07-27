from preprocessing import preprocess_text

sample = """
Program Kreativitas Mahasiswa Artikel Ilmiah (PKM-AI)
bertujuan membantu mahasiswa menulis artikel ilmiah.
"""

print("TEXT ASLI")
print(sample)

print("\nHASIL PREPROCESSING")

tokens = preprocess_text(sample)

print(tokens)