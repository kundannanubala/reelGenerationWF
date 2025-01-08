from langchain_google_community import TextToSpeechTool
import shutil
import os
from core.config import settings
from datetime import datetime

def text_to_speech(text_block):
    
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.GOOGLE_APPLICATION_CREDENTIALS
    llm = TextToSpeechTool()
    llm.name

    speech_file = llm.run(text_block)
    print(speech_file)  # This prints the temp file path

    # Copy the temp file to your desired location
    output_folder = "media/GeneratedAudio"
    os.makedirs(output_folder, exist_ok = True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(output_folder, f"audio_{timestamp}.mp3")
    shutil.copy2(speech_file, output_folder)


def delete_speech_file():
    folder_path = "media/GeneratedAudio"
    if os.path.exists(folder_path):
        for file in os.listdir(folder_path):
            os.remove(os.path.join(folder_path, file))
