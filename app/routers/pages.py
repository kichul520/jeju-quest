from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from app.config import get_settings, Settings

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def home(request: Request, settings: Settings = Depends(get_settings)):
    """메인 페이지 - 지도와 퀘스트 목록"""
    return templates.TemplateResponse(
        "pages/home.html",
        {
            "request": request,
            "title": "제주 퀘스트",
            "kakao_js_key": settings.kakao_js_key,
        }
    )


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """로그인 페이지"""
    return templates.TemplateResponse(
        "pages/login.html",
        {"request": request, "title": "로그인"}
    )


@router.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    """회원가입 페이지"""
    return templates.TemplateResponse(
        "pages/signup.html",
        {"request": request, "title": "회원가입"}
    )


@router.get("/inventory", response_class=HTMLResponse)
async def inventory_page(request: Request):
    """인벤토리 페이지 - 획득한 뱃지/쿠폰"""
    return templates.TemplateResponse(
        "pages/inventory.html",
        {"request": request, "title": "인벤토리"}
    )


@router.get("/quest/{quest_id}", response_class=HTMLResponse)
async def quest_detail(request: Request, quest_id: int):
    """퀘스트 상세 페이지"""
    return templates.TemplateResponse(
        "pages/quest_detail.html",
        {"request": request, "title": "퀘스트", "quest_id": quest_id}
    )
