from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from backend.data_loader import get_dataset_files
from backend.embeddings import index_all_datasets
from backend.query_engine import search_query
import threading
app = FastAPI(title='ChatGPT Prototype API')
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])
datasets = []
@app.on_event('startup')
async def startup_event():
    # Index datasets in a background thread to avoid blocking startup
    def idx():
        global datasets
        datasets = index_all_datasets()
    t = threading.Thread(target=idx, daemon=True)
    t.start()
@app.get('/datasets')
def list_datasets():
    files = get_dataset_files()
    return {'datasets': ['ALL'] + files}
@app.get('/ask')
def ask(q: str = Query(...), dataset: str = Query('ALL')):
    results = search_query(q, dataset=dataset)
    return {'query': q, 'results': results}
