from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # App
    app_name: str = "Jeju Quest"
    debug: bool = False
    secret_key: str = "change-this-secret-key-in-production"

    # Supabase
    supabase_url: str = ""
    supabase_key: str = ""  # service_role key (서버 전용)

    # Kakao Map
    kakao_js_key: str = ""

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()
