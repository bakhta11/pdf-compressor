from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
import subprocess
import uuid
import os

app = FastAPI(title="Nika PDF Compressor")

@app.post("/compress")
async def compress_pdf(file: UploadFile = File(...), quality: str = Form("ebook")):
    # Temporary file paths
    input_filename = f"input_{uuid.uuid4()}.pdf"
    output_filename = f"compressed_{uuid.uuid4()}.pdf"

    # Save uploaded file
    with open(input_filename, "wb") as f:
        f.write(await file.read())

    # Compress PDF using Ghostscript
    try:
        subprocess.run([
            "gs", "-sDEVICE=pdfwrite", "-dCompatibilityLevel=1.4",
            f"-dPDFSETTINGS=/{quality}",
            "-dNOPAUSE", "-dQUIET", "-dBATCH",
            f"-sOutputFile={output_filename}", input_filename
        ], check=True)
    except subprocess.CalledProcessError:
        return {"error": "Compression failed"}

    # Remove original file
    os.remove(input_filename)

    # Return compressed file
    return FileResponse(output_filename, filename="compressed.pdf")
