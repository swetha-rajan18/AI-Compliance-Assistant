import chromadb
from sentence_transformers import SentenceTransformer


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

VECTOR_DB_DIR = "vector_db"


class Retriever:
    def __init__(self):
        self.model = SentenceTransformer(MODEL_NAME)

        self.client = chromadb.PersistentClient(
            path=VECTOR_DB_DIR
        )

        self.collection = self.client.get_collection(
            name="ai_compliance_documents"
        )

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        """
        Retrieve the most relevant policy chunks for a query.
        """

        query_embedding = self.model.encode(
            [query]
        )[0].tolist()

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
        )

        retrieved_chunks = []

        for i in range(len(results["documents"][0])):
            retrieved_chunks.append(
                {
                    "text": results["documents"][0][i],
                    "document_name": results["metadatas"][0][i][
                        "document_name"
                    ],
                    "page_number": results["metadatas"][0][i][
                        "page_number"
                    ],
                    "chunk_id": results["ids"][0][i],
                    "distance": results["distances"][0][i],
                }
            )

        return retrieved_chunks