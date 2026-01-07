"""환경 변수 설정 - Railway 호환 v2"""
import os
from functools import lru_cache
from dataclasses import dataclass

print("=== CONFIG.PY LOADED - VERSION 2 ===")


@dataclass
class Settings:
    """앱 설정 - 환경 변수에서 직접 로드"""
    # App
    app_name: str = "Jeju Quest"
    debug: bool = False
    secret_key: str = "change-this-secret-key-in-production"
    
    # Supabase
    supabase_url: str = ""
    supabase_key: str = ""
    
    # Kakao Map
    kakao_js_key: str = ""
    
    def __post_init__(self):
        """환경 변수에서 값 로드"""
        self.debug = os.environ.get("DEBUG", "false").lower() == "true"
        self.secret_key = os.environ.get("SECRET_KEY", self.secret_key)
        self.supabase_url = os.environ.get("SUPABASE_URL", "")
        self.supabase_key = os.environ.get("SUPABASE_KEY", "")
        self.kakao_js_key = os.environ.get("KAKAO_JS_KEY", "")
        
        # 디버그 출력
        print(f"[Config] KAKAO_JS_KEY loaded: {bool(self.kakao_js_key)} (len={len(self.kakao_js_key)})")
        print(f"[Config] SUPABASE_URL loaded: {bool(self.supabase_url)}")
        print(f"[Config] SUPABASE_KEY loaded: {bool(self.supabase_key)}")


# 캐싱 없이 매번 새로 생성 (환경 변수 변경 반영)
def get_settings() -> Settings:
    return Settings()
