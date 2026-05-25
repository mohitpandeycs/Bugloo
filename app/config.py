from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    GROQ_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None
    SUPABASE_URL: str
    SUPABASE_ANON_KEY: str
    SECRET_KEY: str = "default_secret_key"
    
    class Config:
        env_file = ".env"

settings = Settings()