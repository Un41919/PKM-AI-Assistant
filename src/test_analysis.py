from analysis import word_frequency

documents = [
    """
    Program Kreativitas Mahasiswa bertujuan
    membantu mahasiswa menulis artikel ilmiah.
    """,

    """
    Mahasiswa mengembangkan inovasi dan kreativitas.
    """
]

freq = word_frequency(documents)

print(freq.most_common(20))