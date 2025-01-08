from fastapi import APIRouter
from services.storyGenService import *

router = APIRouter()

@router.get("/generateStory")
def storyGen(context: str):
    story = generate_story(context)
    
    return {"story": story}

@router.get("/generateFlashcard")
def flashcardGen(story: str):
    flashcard = flashcard_generator(story)
    return {"flashcard": flashcard}

@router.get("/saveStoryFlashcard")
def saveStoryFlashcard(story: str, flashcard: str):
    save_story_flashcard(story, flashcard)
    return {"message": "Story and flashcard saved successfully"}

@router.get("/deleteStoryFlashcard")
def deleteStoryFlashcard():
    delete_story_flashcard()
    return {"message":"Story and Flashcard deleted Sucessfully"}