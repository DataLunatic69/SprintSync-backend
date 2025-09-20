from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyUrl, Field

class Settings(BaseSettings):
    DATABASE_URL: AnyUrl
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "openai/gpt-oss-20b"  # Current recommended model
    PORT: int = Field(default=8000, env="PORT")
    PINECONE_API_KEY: str = ""
    PINECONE_ENVIRONMENT: str = ""
    PINECONE_INDEX_NAME: str = "user-skills"
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

# Create a global config instance
config = Settings()