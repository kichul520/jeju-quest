from fastapi import APIRouter, Request, Response, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.database import get_db

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.post("/login")
async def login(
    request: Request,
    response: Response,
    email: str = Form(...),
    password: str = Form(...)
):
    """로그인 처리"""
    db = get_db()

    try:
        result = db.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

        # 세션 쿠키 설정
        response = RedirectResponse(url="/", status_code=303)
        response.set_cookie(
            key="access_token",
            value=result.session.access_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=60 * 60 * 24 * 7  # 7일
        )
        return response

    except Exception as e:
        return templates.TemplateResponse(
            "pages/login.html",
            {
                "request": request,
                "title": "로그인",
                "error": "이메일 또는 비밀번호가 올바르지 않습니다."
            }
        )


@router.post("/signup")
async def signup(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    nickname: str = Form(...)
):
    """회원가입 처리"""
    db = get_db()

    try:
        result = db.auth.sign_up({
            "email": email,
            "password": password,
            "options": {
                "data": {
                    "nickname": nickname
                }
            }
        })

        # 회원가입 후 로그인 페이지로
        return templates.TemplateResponse(
            "pages/login.html",
            {
                "request": request,
                "title": "로그인",
                "message": "가입 완료! 이메일을 확인해주세요."
            }
        )

    except Exception as e:
        return templates.TemplateResponse(
            "pages/signup.html",
            {
                "request": request,
                "title": "회원가입",
                "error": str(e)
            }
        )


@router.post("/logout")
async def logout():
    """로그아웃"""
    response = RedirectResponse(url="/login", status_code=303)
    response.delete_cookie("access_token")
    return response
