from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, TextClip, CompositeVideoClip
import os
from typing import List, Union, Tuple
import logging
import re
from datetime import timedelta

def extract_scene_durations(flashcard: str, total_audio_duration: float = None) -> List[float]:
    """
    Extract durations for each scene based on narrator text length and total audio duration.
    """
    scenes = []
    narrations = []
    total_words = 0
    scene_pattern = r"Scene \d+: "

    # First pass: collect all narrations and count total words
    for line in flashcard.split('\n'):
        if line.startswith("Narrator:"):
            narration = line.replace("Narrator:", "").strip()
            words = len(narration.split())
            narrations.append(words)
            total_words += words

    # Second pass: calculate proportional durations
    if total_audio_duration and narrations:
        for words in narrations:
            # Calculate duration proportionally to the total audio duration
            duration = (words / total_words) * total_audio_duration
            # Ensure minimum duration of 2 seconds per scene
            duration = max(2.0, duration)
            scenes.append(duration)
    else:
        # Fallback to the original word-based calculation if no audio duration
        for words in narrations:
            duration = max(2, words * 0.4)  # Reduced from 0.5 to 0.4 seconds per word
            scenes.append(duration)

    return scenes if scenes else [5]  # Default 5 seconds if no scenes found

def generate_srt_content(flashcard: str, scene_durations: List[float]) -> str:
    """
    Generate SRT subtitle content from flashcard text.
    """
    srt_content = ""
    current_time = 0
    subtitle_index = 1
    
    for line in flashcard.split('\n'):
        if line.startswith("Narrator:"):
            narration = line.replace("Narrator:", "").strip()
            start_time = timedelta(seconds=current_time)
            duration = scene_durations[min(subtitle_index-1, len(scene_durations)-1)]
            end_time = timedelta(seconds=current_time + duration)
            
            srt_content += f"{subtitle_index}\n"
            srt_content += f"{str(start_time).split('.')[0]},000 --> {str(end_time).split('.')[0]},000\n"
            srt_content += f"{narration}\n\n"
            
            current_time += duration
            subtitle_index += 1
    
    return srt_content

def create_subtitle_clips(flashcard: str, scene_durations: List[float], video_size: Tuple[int, int]) -> List[TextClip]:
    """
    Create subtitle clips for the video with improved synchronization.
    """
    subtitle_clips = []
    current_time = 0
    scene_index = 0
    
    for line in flashcard.split('\n'):
        if line.startswith("Narrator:"):
            if scene_index >= len(scene_durations):
                break
                
            narration = line.replace("Narrator:", "").strip()
            duration = scene_durations[scene_index]
            
            # Split long narrations into multiple lines if needed
            words = narration.split()
            if len(words) > 10:
                # Split into chunks of roughly equal length
                mid = len(words) // 2
                narration = ' '.join(words[:mid]) + '\n' + ' '.join(words[mid:])
            
            text_clip = (TextClip(narration, 
                                fontsize=28,  # Slightly smaller font
                                color='white',
                                bg_color='rgba(0,0,0,0.7)',  # More opaque background
                                size=(video_size[0] * 0.9, None),  # 90% of video width
                                method='caption',
                                font='Arial-Bold')  # Bold font for better readability
                        .set_start(current_time)
                        .set_duration(duration)
                        .set_position(('center', 0.85)))  # Position at 85% from top
            
            subtitle_clips.append(text_clip)
            current_time += duration
            scene_index += 1
    
    return subtitle_clips

def create_video_from_images_and_audio(
    image_paths: List[str],
    audio_path: str,
    flashcard: str,
    output_path: str = "generated_videos/output_video.mp4"
) -> str:
    """
    Creates a video by combining images with audio narration and synchronized subtitles.
    """
    try:
        # Validate inputs
        if not image_paths:
            logging.error("No image paths provided")
            return ""
        
        if not os.path.exists(audio_path):
            logging.error(f"Audio file not found: {audio_path}")
            return ""
            
        for img_path in image_paths:
            if not os.path.exists(img_path):
                logging.error(f"Image file not found: {img_path}")
                return ""

        # Load audio file
        audio_clip = AudioFileClip(audio_path)
        
        # Extract durations using actual audio duration
        durations = extract_scene_durations(flashcard, audio_clip.duration)
        
        # Ensure we have durations for all images
        if len(durations) < len(image_paths):
            remaining_duration = audio_clip.duration - sum(durations)
            remaining_scenes = len(image_paths) - len(durations)
            if remaining_duration > 0 and remaining_scenes > 0:
                scene_duration = remaining_duration / remaining_scenes
                durations.extend([scene_duration] * remaining_scenes)
            else:
                durations.extend([3] * (len(image_paths) - len(durations)))
        
        # Adjust durations to match audio length
        total_duration = sum(durations)
        if total_duration > audio_clip.duration:
            scale_factor = audio_clip.duration / total_duration
            durations = [d * scale_factor for d in durations]
        
        # Create video clips from images
        video_clips = []
        current_time = 0
        for img_path, duration in zip(image_paths, durations):
            clip = (ImageClip(img_path)
                   .set_start(current_time)
                   .set_duration(duration))
            video_clips.append(clip)
            current_time += duration
        
        # Concatenate clips and set audio
        final_clip = concatenate_videoclips(video_clips)
        final_clip = final_clip.set_audio(audio_clip)
        
        # Get video dimensions for subtitle positioning
        video_size = final_clip.size
        
        # Generate subtitle clips with improved sync
        subtitle_clips = create_subtitle_clips(flashcard, durations, video_size)
        
        # Generate SRT file
        srt_content = generate_srt_content(flashcard, durations)
        srt_path = output_path.rsplit('.', 1)[0] + '.srt'
        with open(srt_path, 'w', encoding='utf-8') as f:
            f.write(srt_content)
        
        # Combine video with subtitles
        final_clip = CompositeVideoClip([final_clip] + subtitle_clips)
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Write video file
        final_clip.write_videofile(
            output_path,
            fps=24,
            codec='libx264',
            audio_codec='aac',
            remove_temp=True
        )
        
        # Clean up
        final_clip.close()
        audio_clip.close()
        
        return output_path if os.path.exists(output_path) else ""
        
    except Exception as e:
        logging.error(f"Error creating video: {str(e)}")
        return ""