import os
from datetime import datetime
import vertexai
from vertexai.vision_models import ImageGenerationModel
from typing import List, Tuple
import re
from core.config import settings

def generate_image_vertexai(scene: str, story: str) -> str:
    """
    Generates an image based on the scraped content using Vertex AI.
    Returns the path to the locally saved image.
    """
    try:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.GOOGLE_APPLICATION_CREDENTIALS2
        # Initialize Vertex AI
        vertexai.init(project=settings.GOOGLE_CLOUD_PROJECT,location=settings.GOOGLE_CLOUD_REGION2)
        model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")

        # Create a prompt based on the scraped content
        
        prompt = f"""
        This is the story: {story}
        Create a animation style image for this scene: {scene}
        
        Consider the following guidelines:
        1. The image should be visually appealing and relevant to the scene and story
        2. Use a modern and child friendly art style
        3. Ensure the image is suitable for a children audience
        4. Create a balanced composition
        5. Use appropriate lighting and colors
        """

        # Generate the image
        images = model.generate_images(
            prompt=prompt,
            number_of_images=1,
            language="en",
            aspect_ratio="16:9",  # Using widescreen ratio for blog images
            safety_filter_level="block_some",
            person_generation="allow_all",
        )

        if images:
            # Create output directory if it doesn't exist
            output_folder = "GeneratedImages"
            os.makedirs(output_folder, exist_ok=True)

            # Generate unique filename using timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = os.path.join(output_folder, f"image_{timestamp}.png")

            # Save the image locally
            images[0].save(location=output_file, include_generation_parameters=False)
            
            print(f"Generated and saved image to: {output_file}")
            return output_file

        return ""  # Return empty string if no image was generated

    except Exception as e:
        print(f"Error generating image: {str(e)}")
        return ""  # Return empty string on error

def extract_and_generate_scenes(flashcard: str, story: str) -> List[Tuple[str, str]]:
    """
    Extracts scenes from the story text and generates images for each scene.
    Returns a list of tuples containing (scene_number, image_path).
    """
    # Extract scenes using regex
    scene_pattern = r"Scene \d+: (.*?)(?=\n|$)"
    scenes = re.findall(scene_pattern, flashcard)
    
    # Store results
    generated_images = []
    
    # Process each scene
    for index, scene in enumerate(scenes, 1):
        print(f"Processing Scene {index}: {scene}")
        
        # Generate image for the scene
        image_path = generate_image_vertexai(scene, story)
        
        if image_path:
            generated_images.append((f"Scene {index}", image_path))
        else:
            print(f"Failed to generate image for Scene {index}")
    
    return generated_images

