from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from services.videoGenerationService import create_video_from_images_and_audio
from typing import List
from models.videoGenModel import VideoGenerationRequest
router = APIRouter()



@router.post("/generateVideo")
def videoGen(request: VideoGenerationRequest):
    try:
        create_video_from_images_and_audio(
            request.image_paths,
            request.audio_path,
            request.flashcard,
            request.output_path
        )
        return {"message": "Video Generated Successfully!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
