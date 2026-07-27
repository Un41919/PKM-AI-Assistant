from langchain_huggingface import HuggingFaceEmbeddings

from config import EMBEDDING_MODEL


def create_embedding_model():
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )

    return embeddings