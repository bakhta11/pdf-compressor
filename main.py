from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse, HTMLResponse
import subprocess
import os
import uuid

app = FastAPI()

# HTML upload page
@app.get("/", response_class=HTMLResponse)
async def upload_page():
    return """
    <html>
        <head>
            <title>PDF Compressor</title>
        </head>
        <body style="font-family: sans-serif; text-align:center; margin-top:50px;">
            <h2>📄 Upload a PDF to Compress</h2>
            <form action="/compress" enctype="multipart/form-data" method="post">
                <input type="file" name="file" accept="application/pdf" required><br><br>
                <label>Compression Quality:</label>
                <select name="quality">
                    <option value="screen">Screen (Low)</option>
                    <option value="ebook">eBook (Medium)</option>
                    <option value="printer">Printer (High)</option>
                    <option value="prepress">Prepress (Very High)</option>
                </select><br><br>
                <button type="submit">Compress PDF</button>
            </form>
        </body>
    </html>
    """

@app.post("/compress")
async def compress_pdf(file: UploadFile = File(...), quality: str = Form("ebook")):
    # Save uploaded file temporarily
    input_filename = f"input_{uuid.uuid4()}.pdf"
    output_filename = f"compressed_{uuid.uuid4()}.pdf"
    with open(input_filename, "wb") as f:
        f.write(await file.read())

    # Use Ghostscript to compress PDF
    command = [
        "gs",
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        f"-dPDFSETTINGS=/{quality}",
        "-dNOPAUSE",
        "-dQUIET",
        "-dBATCH",
        f"-sOutputFile={output_filename}",
        input_filename
    ]

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError:
        return {"error": "Compression failed. Make sure Ghostscript is installed."}

    # Remove original file
    os.remove(input_filename)

    # Return compressed PDF file for download
    return FileResponse(
        path=output_filename,
        media_type="application/pdf",
        filename="compressed.pdf"
    )