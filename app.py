from fastapi import FastAPI, UploadFile, File
import pdfplumber, tempfile, os

app = FastAPI()

@app.post("/parse/pdf-tables")
async def parse_pdf_tables(file: UploadFile = File(...)):
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp_path = tmp.name
            tmp.write(await file.read())

        tables_out = []
        with pdfplumber.open(tmp_path) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables() or []
                for table in tables:
                    tables_out.append(table)

        return {"tables": tables_out}

    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)
