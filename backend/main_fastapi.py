from fastapi import FastAPI
from pydantic import BaseModel
from agents.receptionist_agent import ReceptionistAgent
from agents.clinical_agent import ClinicalAgent
from loguru import logger
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


receptionist = ReceptionistAgent()
clinical = ClinicalAgent()


class NameIn(BaseModel):
    name: str


class QuestionIn(BaseModel):
    name: str
    question: str


@app.post('/lookup')
def lookup(data: NameIn):
    res = receptionist.ask_initial(data.name)
    return res


@app.post('/ask')
def ask(data: QuestionIn):
    # find patient
    found = receptionist.find_by_name(data.name)
    if found is None:
        return {"error": "patient not found"}
    if isinstance(found, list):
        return {"error": "multiple patients match, please disambiguate"}
    resp = clinical.answer(found, data.question)
    logger.info(f"Answered question for {data.name}")
    return resp