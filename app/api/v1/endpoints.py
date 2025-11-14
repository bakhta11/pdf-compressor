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


from fastapi import APIRouter, UploadFile, File, Query
from fastapi.responses import FileResponse
from app.services.compressor import compress_pdf
from .enums import QualityLevel

router = APIRouter()

@router.post("/compress")
async def compress(
    file: UploadFile = File(...),
    quality: QualityLevel = Query(QualityLevel.medium, description="PDF compression quality")
):
    output_path = await compress_pdf(file, quality)
    return FileResponse(
        output_path,
        media_type="application/pdf",
        filename=output_path.split("/")[-1]
    )
