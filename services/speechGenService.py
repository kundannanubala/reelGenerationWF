from langchain_google_community import TextToSpeechTool
import shutil
import os
from core.config import settings

def text_to_speech(text_block):
    
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.GOOGLE_APPLICATION_CREDENTIALS
    llm = TextToSpeechTool()
    llm.name

    speech_file = llm.run(text_block)
    print(speech_file)  # This prints the temp file path

    # Copy the temp file to your desired location
    output_path = "audio.mp3"
    shutil.copy2(speech_file, output_path)


    
