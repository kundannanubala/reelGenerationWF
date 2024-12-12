from google.cloud import texttospeech
import os
import io

def text_to_speech(text_block):
    try:
        # Explicitly set credentials for text-to-speech
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "texttospeechCredentials.json"
        
        # Initialize Text-to-Speech client
        client = texttospeech.TextToSpeechClient()
        
        # Configure the synthesis request
        synthesis_input = texttospeech.SynthesisInput(text=text_block)
        
        # Build the voice request with a specific voice instead of neutral
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,  # Changed from NEUTRAL to FEMALE
            name="en-US-Standard-C"  # Specific voice name
        )
        
        # Select the type of audio file
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=0.9,  # Slightly slower for children's stories
            pitch=0.0
        )
        
        # Perform the text-to-speech request
        response = client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )
        
        # Create output directory if it doesn't exist
        os.makedirs('generated_audio', exist_ok=True)
        output_path = os.path.join('generated_audio', 'audio.mp3')
        
        # Save the audio file
        with open(output_path, "wb") as out:
            out.write(response.audio_content)
            
        print(f"Successfully generated audio file at: {output_path}")
        return output_path, response.audio_content

    except Exception as e:
        print(f"Error in text_to_speech: {str(e)}")
        return None, None


    
