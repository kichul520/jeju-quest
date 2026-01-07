from supabase import create_client, Client
from app.config import get_settings

settings = get_settings()

# Supabase 클라이언트 (서버 전용)
supabase: Client = create_client(
    settings.supabase_url,
    settings.supabase_key
)


def get_db() -> Client:
    """Supabase 클라이언트 반환"""
    return supabase
