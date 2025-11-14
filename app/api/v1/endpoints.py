#from fastapi import APIRouter, UploadFile, File
#from fastapi.responses import FileResponse
#from app.services.compressor import compress_pdf

#router = APIRouter()

#@router.post("/compress")
#async def compress(file: UploadFile = File(...)):
#    output_path = await compress_pdf(file)

#    return FileResponse(
#        output_path,
#        media_type="application/pdf",
#        filename=output_path.split("/")[-1]
#    )


#from fastapi import APIRouter, UploadFile, File, Query
#from fastapi.responses import FileResponse
#from app.services.compressor import compress_pdf
#from .enums import QualityLevel

#router = APIRouter()

#@router.post("/compress")
#async def compress(
 #   file: UploadFile = File(...),
  #  quality: QualityLevel = Query(QualityLevel.medium, description="PDF compression quality")
#):
#    output_path = await compress_pdf(file, quality)
 #   return FileResponse(
  #      output_path,
   #     media_type="application/pdf",
    #    filename=output_path.split("/")[-1]
    #)

from fastapi import FastAPI, UploadFile, File, Query
import subprocess
import uuid

app = FastAPI()

@app.post("/compress")
async def compress_pdf(
    upload_file: UploadFile = File(...),
    quality: CompressionQuality = Query(..., description="Select compression quality")
):
    # Map user-friendly enum to Ghostscript setting
    quality_setting = QUALITY_MAP[quality.value]

    file_id = uuid.uuid4().hex
    input_path = f"/tmp/{file_id}.pdf"
    output_path = f"/tmp/{file_id}_compressed.pdf"

    with open(input_path, "wb") as f:
        f.write(await upload_file.read())

    cmd = [
        "gs",
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        f"-dPDFSETTINGS={quality_setting}",
        "-dNOPAUSE",
        "-dQUIET",
        "-dBATCH",
        f"-sOutputFile={output_path}",
        input_path
    ]

    subprocess.run(cmd, check=True)

    return {"compressed_file": output_path}
