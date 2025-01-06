from fastapi import APIRouter
from services.storyGenService import generate_story, flashcard_generator

router = APIRouter()

@router.get("/generateStory")
def storyGen(context: str):
    story = generate_story(context)
    
    return {"story": story}

@router.get("/generateFlashcard")
def flashcardGen(story: str):
    flashcard = flashcard_generator(story)
    return {"flashcard": flashcard}
