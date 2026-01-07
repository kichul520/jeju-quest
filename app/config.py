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
        extra="ignore",
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Railway 환경변수 직접 로드 (pydantic이 읽지 못할 경우 대비)
        if not self.kakao_js_key and os.environ.get("KAKAO_JS_KEY"):
            self.kakao_js_key = os.environ.get("KAKAO_JS_KEY", "")
        if not self.supabase_url and os.environ.get("SUPABASE_URL"):
            self.supabase_url = os.environ.get("SUPABASE_URL", "")
        if not self.supabase_key and os.environ.get("SUPABASE_KEY"):
            self.supabase_key = os.environ.get("SUPABASE_KEY", "")
        if not self.secret_key and os.environ.get("SECRET_KEY"):
            self.secret_key = os.environ.get("SECRET_KEY", "")


@lru_cache
def get_settings() -> Settings:
    # 디버그: 환경 변수 직접 확인
    print(f"[DEBUG] KAKAO_JS_KEY from os.environ: {os.environ.get('KAKAO_JS_KEY', 'NOT SET')[:10]}...")
    return Settings()


