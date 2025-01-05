from uvicorn import run
from fastapi import FastAPI
from api import storyGen, audioGen, imageGen, videoGen
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

app.include_router(storyGen.router, tags=["StoryGen"], prefix="/storyGen")
app.include_router(audioGen.router, tags=["AudioGen"], prefix="/audioGen")
app.include_router(imageGen.router, tags=["ImageGen"], prefix="/imageGen")
app.include_router(videoGen.router, tags=["VideoGen"], prefix="/videoGen")

if __name__ == "__main__":
    run(app, host="0.0.0.0", port=8000)

