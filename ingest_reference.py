# Convert nephrology PDF(s) into plain text chunks (or use pre-made txt)
import pdfplumber
from pathlib import Path


IN_PDF = "reference_texts/nephrology_reference.pdf"
OUT_TXT = "reference_texts/nephrology_reference.txt"


if not Path(IN_PDF).exists():
print("Place your nephrology PDF at reference_texts/nephrology_reference.pdf or edit the path.")
else:
text = []
with pdfplumber.open(IN_PDF) as pdf:
for page in pdf.pages:
text.append(page.extract_text() or "")
with open(OUT_TXT, "w", encoding="utf-8") as f:
f.write("\n\n".join(text))
print(f"Wrote extracted text to {OUT_TXT}")