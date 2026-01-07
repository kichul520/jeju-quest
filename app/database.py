from supabase import create_client, Client
from app.config import get_settings
from functools import lru_cache
from typing import Optional

_client: Optional[Client] = None


def get_db() -> Client:
    """Supabase 클라이언트 반환 (lazy initialization with error handling)"""
    global _client

    if _client is not None:
        return _client

    settings = get_settings()

    if not settings.supabase_url or not settings.supabase_key:
        raise ValueError(
            "SUPABASE_URL과 SUPABASE_KEY 환경변수가 설정되어야 합니다. "
            f"URL: {'설정됨' if settings.supabase_url else '미설정'}, "
            f"KEY: {'설정됨' if settings.supabase_key else '미설정'}"
        )

    try:
        _client = create_client(
            settings.supabase_url,
            settings.supabase_key
        )
        print("Supabase 클라이언트 연결 성공")
        return _client
    except Exception as e:
        print(f"Supabase 연결 실패: {e}")
        raise
