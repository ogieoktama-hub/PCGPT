import os
from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels
from sentence_transformers import SentenceTransformer
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
from backend.data_loader import load_all_datasets
from backend.config import QDRANT_HOST, QDRANT_PORT, EMBEDDING_MODEL
qdrant = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
model = SentenceTransformer(EMBEDDING_MODEL)
def index_all_datasets(data_dir=None):
    datasets = load_all_datasets(data_dir)
    created = []
    for dataset_name, df in datasets.items():
        collection_name = dataset_name.replace(' ', '_').lower()
        try:
            qdrant.recreate_collection(
                collection_name=collection_name,
                vectors_config=qmodels.VectorParams(size=model.get_sentence_embedding_dimension(), distance=qmodels.Distance.COSINE)
            )
        except Exception:
            # sometimes recreate fails if collection exists; ignore
            pass
        texts = df.astype(str).apply(lambda row: ' | '.join(row.values.tolist()), axis=1).tolist()
        embeddings = model.encode(texts, show_progress_bar=False)
        points = []
        for i, (emb, payload) in enumerate(zip(embeddings, df.to_dict(orient='records'))):
            points.append(qmodels.PointStruct(id=i, vector=emb.tolist(), payload={'row': payload}))
        qdrant.upsert(collection_name=collection_name, points=points)
        created.append(collection_name)
    return created
if __name__ == '__main__':
    print('Indexing datasets...')
    created = index_all_datasets()
    print('Indexed collections:', created)
