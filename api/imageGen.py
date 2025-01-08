from fastapi import APIRouter, HTTPException
from models.imageGenModel import ImageGenerationResponse
from services.imageGenService import *

router = APIRouter()

@router.get("/generateImage", response_model=ImageGenerationResponse)
async def generate_scenes(flashcard: str, story: str):
    try:
        # Call the service function to generate images for scenes
        generated_scenes = extract_and_generate_scenes(flashcard, story)
        
        # Return the response
        return ImageGenerationResponse(scenes=generated_scenes)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/deleteGeneratedImages")
def deleteGeneratedImages():
    delete_generated_images()
    return {"message": "Generated images deleted successfully"}


