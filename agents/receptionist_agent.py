import json
from loguru import logger
from pathlib import Path


PATIENT_DB = Path("patient_db.json")


class ReceptionistAgent:
    def __init__(self, patient_db_path=PATIENT_DB):
        self.patient_db_path = patient_db_path
        self._load_db()


    def _load_db(self):
        if self.patient_db_path.exists():
            with open(self.patient_db_path, 'r') as f:
                self.patients = json.load(f)
        else:
            self.patients = []


    def find_by_name(self, name):
        logger.info(f"Patient lookup: {name}")
        results = [p for p in self.patients if name.lower() in p['patient_name'].lower()]
        if len(results) == 0:
            logger.warning("No patient found")
            return None
        if len(results) > 1:
            logger.warning("Multiple patients found")
            return results
        return results[0]


    def ask_initial(self, name):
        p = self.find_by_name(name)
        if p is None:
            return {"type":"no_patient","message": "No patient found with that name."}
        if isinstance(p, list):
            return {"type":"multiple","message": "Multiple patients matched.", "matches": p}
        # single
        return {"type":"found","patient": p}


if __name__ == '__main__':
    r = ReceptionistAgent()
    print(r.ask_initial("John"))