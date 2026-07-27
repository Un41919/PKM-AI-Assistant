from rag_pipeline import load_documents, split_documents

from embedding import create_embedding_model

from vector_store import create_vector_store


def build_index():

    print("=" * 80)
    print("Loading Documents...")
    print("=" * 80)

    documents = load_documents()

    print(f"Documents : {len(documents)}")

    print("\nSplitting Documents...")

    chunks = split_documents(documents)

    print(f"Chunks : {len(chunks)}")

    print("\nLoading Embedding Model...")

    embedding_model = create_embedding_model()

    print("\nCreating ChromaDB...")

    create_vector_store(chunks, embedding_model)

    print("\nIndex successfully created.")


if __name__ == "__main__":
    build_index()