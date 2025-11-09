from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import json
from loguru import logger
import os


CHUNKS_FILE = "reference_texts/chunks.json"
INDEX_FILE = "reference_index.faiss"
MODEL_NAME = "all-MiniLM-L6-v2"


class ClinicalAgent:
    def __init__(self):
        self.model = SentenceTransformer(MODEL_NAME)
        self.index = faiss.read_index(INDEX_FILE)
        with open(CHUNKS_FILE, 'r', encoding='utf-8') as f:
            self.chunks = json.load(f)


    def _retrieve(self, query, top_k=3):
        q_emb = self.model.encode([query]).astype('float32')
        D, I = self.index.search(q_emb, top_k)
        results = []
        for idx in I[0]:
            if idx < len(self.chunks):
                results.append(self.chunks[idx]['text'])
                logger.info(f"Retrieved {len(results)} chunks for query")
            return results


    def answer(self, patient, question):
    # RAG: retrieve + simple template
        retrieved = self._retrieve(question, top_k=4)
        context = "\n\n".join(retrieved)
        # For POC we craft a conservative answer using retrieved context + patient info
        answer = (
        f"Patient: {patient['patient_name']} (Dx: {patient['primary_diagnosis']})\n"
        f"Question: {question}\n\n"
        "Based on the reference material, relevant excerpts:\n" + context[:2000]
        + "\n\nNote: This is an educational POC. Consult clinicians for medical decisions."
        )
        # Return with citations (we simply point to chunk indices)
        citations = [f"chunk_{i}" for i in range(min(len(retrieved),4))]
        return {"answer": answer, "citations": citations}


if __name__ == '__main__':
    ca = ClinicalAgent()
    with open('patient_db.json') as f:
        patient = json.load(f)[0]
        resp = ca.answer(patient, "What causes leg swelling in CKD?")
        print(resp['answer'][:800])