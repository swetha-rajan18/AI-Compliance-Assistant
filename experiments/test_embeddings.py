from sentence_transformers import SentenceTransformer


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


model = SentenceTransformer(MODEL_NAME)

texts = [
    "What is the purpose of the NIST AI Risk Management Framework?",
    "High-risk artificial intelligence systems are subject to specific requirements.",
]

embeddings = model.encode(texts)

print(f"Number of texts: {len(texts)}")
print(f"Embedding shape: {embeddings.shape}")
print(f"Embedding dimension: {embeddings.shape[1]}")
print(f"First embedding values: {embeddings[0][:10]}")