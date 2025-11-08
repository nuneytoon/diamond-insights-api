from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # API Configuration
    api_name: str = "Diamond Insights API"
    api_version: str = "1.0.0"
    
    # External API Settings - these assigned values are fallbacks
    api_sports_url: str = "https://api.example.com"
    api_sports_key: str = "your-api-key-here"
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # Ignore extra fields in .env file


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()

