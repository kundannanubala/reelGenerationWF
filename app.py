from services.storyGenerationService import generate_story, flashcard_generator
from services.textToSpeechService import text_to_speech
from services.textToImageService import extract_and_generate_scenes
import os
from google.cloud import aiplatform
from core.config import settings

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

# flashcard = """Narrator: Barnaby Bear loved blueberries and would eat a lot of them.
# Scene 1: Barnaby Bear eating blueberries.

# Narrator: One day, Barnaby found a huge blueberry bush, bigger than his house!
# Scene 2: Barnaby Bear standing next to a giant blueberry bush.

# Narrator:  The berries were enormous! Barnaby climbed the bush and began to eat.
# Scene 3: Barnaby Bear climbing the giant blueberry bush and eating berries.

# Narrator: The bush started to tickle and shake, making Barnaby fall into a pile of fluffy clouds.
# Scene 4: Barnaby Bear falling from the bush into a pile of clouds.

# Narrator: Barnaby bounced and laughed on the clouds.
# Scene 5: Barnaby Bear bouncing and laughing on the clouds.

# Narrator: He floated back down and landed next to another giant blueberry!
# Scene 6: Barnaby Bear landing next to another giant blueberry."""

# story = """Barnaby Bear loved blueberries.  He'd gobble them by the bucketful! One sunny morning, Barnaby found a giant blueberry bush, taller than his house!  The berries were as big as his paws!  He climbed up, up, up, and started munching.  Suddenly, the bush began to tickle!  It giggled and shook, sending Barnaby tumbling into a pile of fluffy clouds.  He bounced and bounced, laughing until his tummy hurt.  Then, whoosh! He floated gently back down, landing right beside another giant blueberry!"""
