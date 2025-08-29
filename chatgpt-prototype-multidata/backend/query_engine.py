from qdrant_client import QdrantClient
from backend.embeddings import model
from backend.config import QDRANT_HOST, QDRANT_PORT
qdrant = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
def search_query(user_query, dataset=None, top_k=5):
    vec = model.encode([user_query])[0]
    try:
        cols = [c.name for c in qdrant.get_collections().collections]
    except Exception:
        cols = []
    targets = [dataset] if dataset and dataset != 'ALL' else cols
    results = []
    for collection in targets:
        try:
            hits = qdrant.search(collection_name=collection, query_vector=vec, limit=top_k)
            for h in hits:
                results.append({'collection': collection, 'score': h.score, 'payload': h.payload})
        except Exception:
            pass
    return results
