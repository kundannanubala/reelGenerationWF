from pydantic import BaseModel
from typing import List

class VideoGenerationRequest(BaseModel):
    image_paths: List[str]
    audio_path: str
    flashcard: str
    output_path: str = "output_video.mp4"