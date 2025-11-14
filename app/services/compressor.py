
#import subprocess
#import uuid
#import os

#async def compress_pdf(upload_file):
    # generate unique file names
#    file_id = uuid.uuid4().hex
 #   input_path = f"/tmp/{file_id}.pdf"
  #  output_path = f"/tmp/{file_id}_compressed.pdf"

   # # save uploaded file
    #with open(input_path, "wb") as f:
     #   f.write(await upload_file.read())

    # ghostscript compression command
    #cmd = [
     #   "gs",
      #  "-sDEVICE=pdfwrite",
       # "-dCompatibilityLevel=1.4",
        #"-dPDFSETTINGS=/ebook",  # compression level
        #"-dNOPAUSE",
        #"-dQUIET",
        #"-dBATCH",
        #f"-sOutputFile={output_path}",
        #input_path
    #]

    #subprocess.run(cmd, check=True)

    #return output_path

import subprocess
import uuid

QUALITY_MAP = {
    "Low": "/screen",
    "Medium": "/ebook",
    "High": "/printer",
    "Very High": "/prepress"
}

async def compress_pdf(upload_file, quality):
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

    return output_path
