from typing import Dict

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from models.transcribe_model import GoogleSTTStrategy, Transcriber

app = FastAPI()


@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    transcription = await transcribe_file(file)
    print(file.filename)
    print(transcription)
    return JSONResponse(content={"transcription": transcription})

async def transcribe_file(file: UploadFile) -> str:
    transcriber = Transcriber(GoogleSTTStrategy())
    transcription = await transcriber.transcribe(file)
    return transcription
