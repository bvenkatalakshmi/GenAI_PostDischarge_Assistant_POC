1. Create a virtualenv: `python -m venv .venv && source .venv/bin/activate`
2. Install: `pip install -r requirements.txt`
3. Generate dummy patients: `python generate_dummy_data.py`
4. Put nephrology reference text into `reference_texts/nephrology_reference.txt` (or change path in `ingest_reference.py`).
5. Build vector store: `python build_vector_store.py`
6. Run backend: `uvicorn backend.main_fastapi:app --reload --port 8000`
7. Run frontend: `streamlit run frontend/streamlit_app.py`