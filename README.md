# AI-Powered Children's Story Generator

A comprehensive application that generates children's stories and converts them into multimedia content using various AI services from Google Cloud Platform.

## 🌟 Features

- Story Generation using Gemini 1.5 Pro
- Text-to-Speech Narration
- AI Image Generation for Story Scenes
- Automated Video Creation from Generated Content
- Flashcard Generation for Story Scenes

## 🛠️ Technologies Used

- Google Cloud Platform Services:
  - Vertex AI (Gemini 1.5 Pro)
  - Text-to-Speech API
  - Imagen 3.0 for Image Generation
- LangChain Framework
- MoviePy for Video Generation
- Python 3.x

## 📋 Prerequisites

- Python 3.x
- Google Cloud Platform Account
- Required API Credentials:
  - Google Cloud Service Account Credentials
  - Vertex AI API Access
  - Text-to-Speech API Access

## 🚀 Installation

1. Clone the repository:
```bash
git clone <repository-url>
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables in `.env` file:
```plaintext
GOOGLE_APPLICATION_CREDENTIALS=path/to/credentials.json
GOOGLE_APPLICATION_CREDENTIALS2=path/to/credentials2.json
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_REGION=your-region
GOOGLE_CLOUD_REGION2=your-region-2
```

## 💻 Usage

1. Initialize the application:
```python
from app import generate_story, flashcard_generator, text_to_speech, extract_and_generate_scenes
```

2. Generate a story:
```python
context = "Your story context here"
story = generate_story(context)
```

3. Generate flashcards and multimedia content:
```python
flashcard = flashcard_generator(story)
text_to_speech(story)
extract_and_generate_scenes(flashcard, story)
```

## 🎯 Project Structure

- `app.py` - Main application entry point
- `services/`
  - `storyGenerationService.py` - Story and flashcard generation
  - `textToSpeechService.py` - Audio narration generation
  - `textToImageService.py` - AI image generation
  - `videoGenerationService.py` - Video compilation
- `core/`
  - `config.py` - Configuration management

## 📝 Output

The application generates:
- A written story in children's book style
- Flashcards with scene descriptions
- Audio narration (MP3 format)
- AI-generated images for each scene
- A compiled video with images and narration

## 🔒 Security Notes

- Keep your Google Cloud credentials secure
- Do not commit credential files to version control
- Use environment variables for sensitive information





## 📞 Support

kundannaubala@gmail.com
