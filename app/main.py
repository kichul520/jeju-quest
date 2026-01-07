from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager

from app.config import get_settings
from app.routers import pages, auth, quests


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 시작 시 실행
    print("Jeju Quest 서버 시작!")
    yield
    # 종료 시 실행
    print("Jeju Quest 서버 종료!")


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
