from services.storyGenService import generate_story, flashcard_generator
from services.speechGenService import text_to_speech
from services.imageGenService import extract_and_generate_scenes
from services.videoGenService import create_video_from_images_and_audio
import os
from google.cloud import aiplatform
from core.config import settings
import glob

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.GOOGLE_APPLICATION_CREDENTIALS

# Initialize the Vertex AI client
aiplatform.init(project=settings.GOOGLE_CLOUD_PROJECT,location=settings.GOOGLE_CLOUD_REGION)

context = "A toddler lost his loose tooth and is crying, but his mom is comforting him and motivates him to look on the bright side as new strong teeth grow in"
story = generate_story(context)
print(story)
flashcard = flashcard_generator(story)
print(flashcard)
text_to_speech(story)

extract_and_generate_scenes(flashcard,story)

# Get all PNG images from the generated_blog_images folder
image_paths = sorted(glob.glob("generated_blog_images/*.png"))

# Create video from images and audio
video_path = create_video_from_images_and_audio(
    image_paths=image_paths,
    audio_path="audio.mp3", 
    flashcard=flashcard, 
    output_path="output_video.mp4"

)

if video_path:
    print(f"Video created successfully at: {video_path}")
else:
    print("Failed to create video")



# story = """Barnaby Bear loved blueberries.  He'd gobble them by the bucketful! One sunny morning, Barnaby found a giant blueberry bush, taller than his house!  The berries were as big as his paws!  He climbed up, up, up, and started munching.  Suddenly, the bush began to tickle!  It giggled and shook, sending Barnaby tumbling into a pile of fluffy clouds.  He bounced and bounced, laughing until his tummy hurt.  Then, whoosh! He floated gently back down, landing right beside another giant blueberry!"""
# flashcard = """
# Narrator: Barnaby the bunny is bouncing by a brook.
# Scene 1: Barnaby bouncing beside a babbling brook.

# Narrator: Shiny pebbles wink in the sun.
# Scene 2: Pebbles shining in the sun.

# Narrator: Barnaby sees a bright blue butterfly.
# Scene 3: Barnaby spotting a blue butterfly.

# Narrator: The butterfly lands on a dandelion.
# Scene 4: Butterfly landing on a dandelion.

# Narrator: Barnaby hops closer to the butterfly.
# Scene 5: Barnaby hopping closer, wiggling his nose.

# Narrator: The butterfly tickles Barnaby's whiskers.
# Scene 6: Butterfly tickling Barnaby's whiskers.

# Narrator: Barnaby giggles.
# Scene 7: Barnaby giggling.

# Narrator: The butterfly flies to some pansies.
# Scene 8: Butterfly flying to purple pansies.

# Narrator: Barnaby follows the butterfly.
# Scene 9: Barnaby following, tail bobbing.

# Narrator: It is a wonderful, sunny day.
# Scene 10: Sunny day scene  Barnaby and the butterfly.
# """