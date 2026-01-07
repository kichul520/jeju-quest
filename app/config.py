from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
import os


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

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # Railway 등 추가 환경 변수 무시
    )


@lru_cache
def get_settings() -> Settings:
    # 디버그: 환경 변수 직접 확인
    print(f"[DEBUG] KAKAO_JS_KEY from os.environ: {os.environ.get('KAKAO_JS_KEY', 'NOT SET')[:10]}...")
    return Settings()

