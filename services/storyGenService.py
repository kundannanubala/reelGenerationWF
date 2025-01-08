from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
import os
from langchain.schema.output_parser import StrOutputParser
from core.config import settings
import os
from datetime import datetime


def story_prompt_template():
    return """
    You are a storyteller. You are given a {context} and you need to generate a story that is 100 words long.
    The story should be in the style of a children's book.
    """

def flashcard_prompt_template():
    return """
    You are a flashcard generator. You are given a {story} and you need to break it down into a flashcard.
    The Scene should have description enough to generate an image. 
    Example output Format:
    Narrator:The story is about a man who is walking in the park.
    Scene 1: The man is walking in the park.
    Narrator: He says "Hello" to the park
    Scene 2: The man is saying "Hello" to the park.
    """


def generate_story(context):
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-002")
    llm.name

    prompt = ChatPromptTemplate.from_template(story_prompt_template())
    try:
        chain = prompt | llm | StrOutputParser()
        return chain.invoke({"context": context})
    
    except Exception as e:
        return f"An error occurred: {str(e)}"


def flashcard_generator(story):
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-002")
    llm.name

    prompt = ChatPromptTemplate.from_template(flashcard_prompt_template())
    try:
        context = {"story": lambda x: story}
        chain = (
            context
            | prompt
            | llm
            | StrOutputParser()
        )

        return chain.invoke(prompt)
    
    except Exception as e:
        return f"An error occurred: {str(e)}"
    
def save_story_flashcard(story, flashcard):
    # Create output directory if it doesn't exist   
    output_folder = "media"
    os.makedirs(output_folder, exist_ok=True)

    # Generate unique filename using timestamp
    
    output_file = os.path.join(output_folder, f"story&flashcard.txt")

    with open(output_file, "w") as f:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        f.write("timeStamp:"f"{timestamp}")
        f.write("\n\n=== STORY ===\n\n")
        f.write(story)
        f.write("\n\n=== FLASHCARD ===\n\n")
        f.write(flashcard)

def delete_story_flashcard():
    os.remove("media/story&flashcard.txt")
