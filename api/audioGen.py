from fastapi import APIRouter
from services.speechGenService import *

router = APIRouter()

@router.get("/generateAudio")
def audioGen(text: str):
    text_to_speech(text)
    return {"audio": "audio.mp3"}

@router.get("/deleteAudio")
def deleteAudio():
    delete_speech_file()
    return {"message": "Audio deleted successfully"}

