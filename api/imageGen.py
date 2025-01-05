from fastapi import APIRouter
from services.textToImageService import extract_and_generate_scenes

router = APIRouter()

@router.get("/generateImage")
def imageGen(text: str):
    extract_and_generate_scenes(text, text)
    return {"Images Generated Successfully!"}
