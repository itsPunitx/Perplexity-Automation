import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Perplexity Automation API"
    debug: bool = False
    environment: str = os.getenv("ENVIRONMENT", "production")
    
    # Automation settings
    default_timeout: int = 30
    browser_headless: bool = True
    max_retries: int = 3
    
    class Config:
        env_file = ".env"

settings = Settings()