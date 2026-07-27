from embedding import create_embedding_model

embedding_model = create_embedding_model()

vector = embedding_model.embed_query(
    "Berapa maksimal anggota tim PKM?"
)

print(f"Vector dimension : {len(vector)}")

print(vector[:10])