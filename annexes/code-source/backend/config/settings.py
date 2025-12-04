# config/settings.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Base de données
    MONGODB_URL: str
    DATABASE_NAME: str = "zamapay_db"
    
    # API Keys
    GEMINI_API_KEY: str
    GOOGLE_CLOUD_PROJECT_ID: str
    
    # Sécurité
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
