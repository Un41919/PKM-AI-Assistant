from langchain_text_splitters import RecursiveCharacterTextSplitter


def create_text_splitter():
    """
    Membuat text splitter untuk dokumen PKM.

    Konfigurasi:
    - chunk_size      : 450 karakter
    - chunk_overlap   : 80 karakter
    - separator dibuat mengikuti struktur dokumen PDF
    """

    splitter = RecursiveCharacterTextSplitter(

        chunk_size=450,

        chunk_overlap=80,

        length_function=len,

        separators=[
            "\n\n",
            "\n",
            ". ",
            "; ",
            ": ",
            ", ",
            " ",
            ""
        ],

        keep_separator=True

    )

    return splitter