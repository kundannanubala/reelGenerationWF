from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    GOOGLE_APPLICATION_CREDENTIALS: str = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    GOOGLE_APPLICATION_CREDENTIALS2: str = os.getenv("GOOGLE_APPLICATION_CREDENTIALS2")
    GOOGLE_CLOUD_PROJECT: str = os.getenv("GOOGLE_CLOUD_PROJECT")
    GOOGLE_CLOUD_REGION: str = os.getenv("GOOGLE_CLOUD_REGION")
    GOOGLE_CLOUD_REGION2: str = os.getenv("GOOGLE_CLOUD_REGION2")

    class Config:
        env_file = ".env"


settings = Settings()