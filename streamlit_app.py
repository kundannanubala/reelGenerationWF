import streamlit as st
from services.storyGenerationService import generate_story, flashcard_generator
from services.textToSpeechService import text_to_speech
from services.textToImageService import extract_and_generate_scenes
from services.videoGenerationService import create_video_from_images_and_audio
import os
from google.cloud import aiplatform
from core.config import settings
import glob

# Page config
st.set_page_config(
    page_title="AI Children's Story Generator",
    page_icon="📚",
    layout="wide"
)

# Initialize Google Cloud credentials and Vertex AI
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.GOOGLE_APPLICATION_CREDENTIALS
aiplatform.init(project=settings.GOOGLE_CLOUD_PROJECT, location=settings.GOOGLE_CLOUD_REGION)

# Title and description
st.title("📚 AI Children's Story Generator")
st.markdown("""
This app generates children's stories complete with narration, images, and video using AI technology.
Simply enter your story context below to get started!
""")

# User input
story_context = st.text_area(
    "Enter your story context",
    placeholder="Example: A toddler lost his loose tooth and is crying, but his mom is comforting him...",
    height=100
)

if st.button("Generate Story"):
    if story_context:
        with st.spinner("Generating story..."):
            # Story generation
            story = generate_story(story_context)
            st.subheader("Generated Story")
            st.write(story)
            
            # Flashcard generation
            with st.spinner("Generating scene flashcards..."):
                flashcard = flashcard_generator(story)
                st.subheader("Story Scenes")
                for scene in flashcard.split('\n\n'):
                    if scene.strip():
                        st.markdown(f"- {scene}")
            
            # Text to speech
            with st.spinner("Generating audio narration..."):
                audio_path, audio_content = text_to_speech(story)
                if audio_path and audio_content:
                    st.subheader("Story Narration")
                    st.audio(audio_content, format='audio/mp3')
                    
                    # Continue with image generation...
                else:
                    st.error("Failed to generate audio narration")
                    st.stop()
            
            # Image generation
            with st.spinner("Generating scene images..."):
                st.subheader("Generated Scene Images")
                col1, col2 = st.columns(2)
                
                # Extract and generate scenes
                scenes = extract_and_generate_scenes(flashcard, story)
                
                # Get all generated images
                image_paths = sorted(glob.glob("generated_blog_images/*.png"))
                
                # Display images with their corresponding scenes
                for idx, (image_path, scene) in enumerate(zip(image_paths, flashcard.split('\n\n'))):
                    if idx % 2 == 0:
                        with col1:
                            st.image(image_path, caption=scene.strip())
                    else:
                        with col2:
                            st.image(image_path, caption=scene.strip())
            
            # Video generation
            with st.spinner("Creating final video..."):
                # Create a directory for videos if it doesn't exist
                os.makedirs('generated_videos', exist_ok=True)
                video_output_path = os.path.join('generated_videos', 'output_video.mp4')
                
                video_path = create_video_from_images_and_audio(
                    image_paths=image_paths,
                    audio_path=os.path.join('generated_audio', 'audio.mp3'),  # Updated audio path
                    flashcard=flashcard,
                    output_path=video_output_path
                )
                
                if video_path and os.path.exists(video_path):
                    st.subheader("Final Story Video")
                    # Read the video file as bytes
                    with open(video_path, 'rb') as video_file:
                        video_bytes = video_file.read()
                    st.video(video_bytes)
                else:
                    st.error("Failed to create video")
    else:
        st.error("Please enter a story context first!")

# Add footer
st.markdown("---")
st.markdown("Created with ❤️ using Streamlit and Google Cloud AI") 