from fastapi import APIRouter
from services.textToSpeechService import text_to_speech

router = APIRouter()

@router.get("/generateAudio")
def audioGen(text: str):
    text_to_speech(text)
    return {"audio": "audio.mp3"}
