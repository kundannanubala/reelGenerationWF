from pydantic import BaseModel
from typing import List, Tuple

class ImageGenerationRequest(BaseModel):
    flashcard: str
    story: str

class ImageGenerationResponse(BaseModel):
    scenes: List[Tuple[str, str]]
