"""
Application configuration.

Responsibilities:
- Load environment variables from .env
- Define configuration values: chunk_size, chunk_overlap, top_k, model_name
- Expose a single config object (or class) that other modules import
- API keys, model settings, and tunable parameters live here
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    openai_api_key: str = Field(...)
    embedding_model: str = Field(default="text-embedding-3-small")
    llm_model: str = Field(default="gpt-4o-mini")
    chunk_size: int = Field(default=1000)
    chunk_overlap: int = Field(default=200)
    top_k: int = Field(default=5)
    index_dir: str = Field(default="index")
    data_dir: str = Field(default="data")
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()