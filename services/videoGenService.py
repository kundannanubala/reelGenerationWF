from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
import os
from typing import List
import logging
import re

def extract_scene_durations(flashcard: str) -> List[float]:
    """
    Extract durations for each scene based on narrator text length.
    """
    scenes = []
    current_narration = ""
    scene_pattern = r"Scene \d+: "

    for line in flashcard.split('\n'):
        if line.startswith("Narrator:"):
            current_narration = line.replace("Narrator:", "").strip()
        elif re.match(scene_pattern, line):
            # Calculate approximate duration based on word count
            words = len(current_narration.split())
            duration = max(3, words * 0.5)  # Assume 0.5 seconds per word, minimum 3 seconds
            scenes.append(duration)
    
    return scenes if scenes else [5]  # Default 5 seconds if no scenes found

def create_video_from_images_and_audio(
    image_paths: List[str],
    audio_path: str,
    flashcard: str,
    output_path: str = "output_video.mp4"
) -> str:
    """
    Creates a video by combining images with audio narration.
    
    Args:
        image_paths: List of paths to the images
        audio_path: Path to the audio file
        flashcard: Flashcard text containing scene descriptions and narration
        output_path: Path where the output video will be saved
        
    Returns:
        str: Path to the output video file or empty string if error occurs
    """
    try:
        # Validate inputs
        if not image_paths:
            raise ValueError("No image paths provided")
        
        if not os.path.exists(audio_path):
            raise ValueError(f"Audio file not found: {audio_path}")
            
        for img_path in image_paths:
            if not os.path.exists(img_path):
                raise ValueError(f"Image file not found: {img_path}")

        # Extract durations from flashcard
        durations = extract_scene_durations(flashcard)
        
        # Ensure we have durations for all images
        if len(durations) < len(image_paths):
            durations.extend([5] * (len(image_paths) - len(durations)))

        # Load audio file
        audio_clip = AudioFileClip(audio_path)
        
        # Create video clips from images
        video_clips = []
        for img_path, duration in zip(image_paths, durations):
            clip = ImageClip(img_path).set_duration(duration)
            video_clips.append(clip)
        
        # Rest of the function remains the same
        final_clip = concatenate_videoclips(video_clips)
        final_clip = final_clip.set_audio(audio_clip)
        
        if final_clip.duration > audio_clip.duration:
            final_clip = final_clip.set_duration(audio_clip.duration)
        
        os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
        
        final_clip.write_videofile(
            output_path,
            fps=24,
            codec='libx264',
            audio_codec='aac',
            remove_temp=True
        )
        
        final_clip.close()
        audio_clip.close()
        
        return output_path
        
    except Exception as e:
        logging.error(f"Error creating video: {str(e)}")
        return ""