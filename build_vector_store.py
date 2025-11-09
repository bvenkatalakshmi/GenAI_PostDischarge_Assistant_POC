from sentence_transformers import SentenceTransformer
import numpy as np
import os
import json
from pathlib import Path
import faiss


MODEL_NAME = "all-MiniLM-L6-v2"
REF_TXT = "reference_texts/nephrology_reference.txt"
CHUNKS_FILE = "reference_texts/chunks.json"
INDEX_FILE = "reference_index.faiss"
EMB_FILE = "reference_embeddings.npy"


# basic text splitting


def chunk_text(text, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = words[i:i+chunk_size]
        chunks.append(" ".join(chunk))
        i += chunk_size - overlap
        return chunks


if not Path(REF_TXT).exists():
    raise SystemExit(f"Put nephrology_reference.txt at {REF_TXT}")


text = Path(REF_TXT).read_text(encoding="utf-8")
chunks = chunk_text(text)


model = SentenceTransformer(MODEL_NAME)
embs = model.encode(chunks, show_progress_bar=True)


# build FAISS index
dim = embs.shape[1]
index = faiss.IndexFlatL2(dim)
index.add(np.array(embs, dtype='float32'))
faiss.write_index(index, INDEX_FILE)
np.save(EMB_FILE, embs)


# save chunks with ids
with open(CHUNKS_FILE, "w", encoding="utf-8") as f:
    json.dump([{"id": i, "text": chunks[i]} for i in range(len(chunks))], f, indent=2)


print("Built FAISS index and saved chunks")