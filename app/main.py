from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
import os

from app.config import get_settings
from app.routers import pages, auth, quests


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 시작 시 환경변수 검증
    settings = get_settings()
    print(f"=== Jeju Quest 서버 시작 ===")
    print(f"DEBUG: {settings.debug}")
    print(f"SUPABASE_URL: {'설정됨' if settings.supabase_url else '미설정!'}")
    print(f"SUPABASE_KEY: {'설정됨' if settings.supabase_key else '미설정!'}")
    print(f"KAKAO_JS_KEY: {'설정됨' if settings.kakao_js_key else '미설정!'}")
    print(f"PORT: {os.environ.get('PORT', '8000')}")
    yield
    print("=== Jeju Quest 서버 종료 ===")


settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    lifespan=lifespan,
)

# 정적 파일 서빙
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# 템플릿 설정
templates = Jinja2Templates(directory="app/templates")

# 라우터 등록
app.include_router(pages.router)
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(quests.router, prefix="/api/quests", tags=["quests"])


# 헬스체크 엔드포인트 (Railway용)
@app.get("/health")
async def health_check():
    return {"status": "ok"}


# 전역 템플릿 컨텍스트
@app.middleware("http")
async def add_global_context(request: Request, call_next):
    request.state.settings = settings
    response = await call_next(request)
    return response
