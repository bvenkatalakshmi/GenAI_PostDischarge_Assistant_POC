import json
from faker import Faker
import random
from datetime import datetime, timedelta


fake = Faker()


DIAGNOSES = [
"Chronic Kidney Disease Stage 2",
"Chronic Kidney Disease Stage 3",
"Acute Kidney Injury",
"Nephrolithiasis",
"Nephrotic Syndrome",
]


MEDS = [
["Lisinopril 10mg daily", "Furosemide 20mg twice daily"],
["Metoprolol 25mg daily"],
["Atorvastatin 10mg nightly"],
["Amlodipine 5mg daily"],
]


OUTFILE = "patient_db.json"


patients = []
for i in range(30):
    name = fake.name()
    discharge_date = (datetime.now() - timedelta(days=random.randint(1, 200))).strftime("%Y-%m-%d")
    diag = random.choice(DIAGNOSES)
    meds = random.choice(MEDS)
    patient = {
    "id": i+1,
    "patient_name": name,
    "discharge_date": discharge_date,
    "primary_diagnosis": diag,
    "medications": meds,
    "dietary_restrictions": "Low sodium (2g/day)",
    "follow_up": "Nephrology clinic in 2 weeks",
    "warning_signs": "Swelling, shortness of breath, decreased urine output",
    "discharge_instructions": "Monitor blood pressure daily, weigh yourself daily",
    }
    patients.append(patient)


with open(OUTFILE, "w") as f:
    json.dump(patients, f, indent=2)


print(f"Wrote {len(patients)} dummy patient records to {OUTFILE}")