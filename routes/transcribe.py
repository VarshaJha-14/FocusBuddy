"""
routes/transcribe.py — Voice transcription via Groq Whisper.

POST /transcribe → Receives audio file, returns transcribed text.
"""

import os
import logging
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from groq import Groq

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/transcribe")
async def transcribe(request: Request):
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key or api_key == "your_groq_api_key_here":
        return JSONResponse({"text": "", "error": "No API key configured for transcription."})
        
    client = Groq(api_key=api_key)
    
    form = await request.form()
    audio_file = form.get("audio")
    if not audio_file:
        return JSONResponse({"text": "", "error": "No audio received"})
    
    audio_bytes = await audio_file.read()
    
    try:
        transcription = client.audio.transcriptions.create(
            file=("recording.webm", audio_bytes, "audio/webm"),
            model="whisper-large-v3-turbo",
            response_format="text"
        )
        return JSONResponse({"text": str(transcription)})
    except Exception as e:
        logger.error(f"Transcription failed: {e}")
        return JSONResponse({"text": "", "error": f"Transcription failed: {str(e)}"})
