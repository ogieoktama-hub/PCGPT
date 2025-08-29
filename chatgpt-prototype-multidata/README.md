# chatgpt-prototype-multidata
Minimal GitHub-ready prototype for a ChatGPT-like assistant over multiple CSV/XLSX datasets.

## Quickstart (local)
1. Copy your datasets (CSV/XLS/XLSX) into the `data/` folder.
2. Start Qdrant (recommended via Docker):
   ```bash
   docker run -p 6333:6333 qdrant/qdrant
   ```
3. Backend:
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate   # or .\.venv\Scripts\activate on Windows (PowerShell)
   pip install -r requirements.txt
   python embeddings.py   # indexes files inside ../data/
   uvicorn app:app --reload --port 8000
   ```
4. Frontend:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
5. Open: http://localhost:5173
