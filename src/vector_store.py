from langchain_chroma import Chroma

from config import VECTOR_DB_DIR


def create_vector_store(chunks, embedding_model):
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=str(VECTOR_DB_DIR)
    )

    return vector_store