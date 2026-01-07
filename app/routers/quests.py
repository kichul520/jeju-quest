from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional
import math

from app.database import get_db

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


class LocationCheck(BaseModel):
    quest_id: int
    latitude: float
    longitude: float


class AnswerSubmit(BaseModel):
    quest_id: int
    answer: str


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """두 좌표 간 거리 계산 (미터)"""
    R = 6371000  # 지구 반지름 (미터)

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


@router.get("/list")
async def get_quests(request: Request):
    """퀘스트 목록 조회 (HTMX용)"""
    db = get_db()

    result = db.table("quests").select("*").eq("is_active", True).execute()

    return templates.TemplateResponse(
        "components/quest_list.html",
        {"request": request, "quests": result.data}
    )


@router.get("/{quest_id}")
async def get_quest(quest_id: int):
    """단일 퀘스트 조회"""
    db = get_db()

    result = db.table("quests").select("*").eq("id", quest_id).single().execute()

    if not result.data:
        raise HTTPException(status_code=404, detail="퀘스트를 찾을 수 없습니다")

    return result.data


@router.post("/check-location")
async def check_location(request: Request, data: LocationCheck):
    """위치 확인 - 퀘스트 반경 내인지 체크"""
    db = get_db()

    # 퀘스트 정보 조회
    result = db.table("quests").select("*").eq("id", data.quest_id).single().execute()

    if not result.data:
        raise HTTPException(status_code=404, detail="퀘스트를 찾을 수 없습니다")

    quest = result.data

    # 거리 계산
    distance = calculate_distance(
        data.latitude, data.longitude,
        quest["latitude"], quest["longitude"]
    )

    # 50m 반경 체크
    is_in_range = distance <= 50

    return templates.TemplateResponse(
        "components/quest_challenge.html",
        {
            "request": request,
            "quest": quest,
            "is_in_range": is_in_range,
            "distance": round(distance)
        }
    )


@router.post("/submit-answer")
async def submit_answer(request: Request, data: AnswerSubmit):
    """퀴즈 정답 제출"""
    db = get_db()

    # 퀘스트 정보 조회
    result = db.table("quests").select("*").eq("id", data.quest_id).single().execute()

    if not result.data:
        raise HTTPException(status_code=404, detail="퀘스트를 찾을 수 없습니다")

    quest = result.data

    # 정답 확인 (대소문자 무시)
    is_correct = data.answer.strip().lower() == quest["answer"].strip().lower()

    if is_correct:
        # TODO: 포인트 적립, 완료 기록 저장
        pass

    return templates.TemplateResponse(
        "components/quest_result.html",
        {
            "request": request,
            "quest": quest,
            "is_correct": is_correct,
            "points": quest.get("points", 100) if is_correct else 0
        }
    )


@router.get("/nearby")
async def get_nearby_quests(latitude: float, longitude: float, radius: float = 1000):
    """주변 퀘스트 조회 (반경 내)"""
    db = get_db()

    # 모든 활성 퀘스트 조회 후 거리 필터링
    result = db.table("quests").select("*").eq("is_active", True).execute()

    nearby = []
    for quest in result.data:
        distance = calculate_distance(
            latitude, longitude,
            quest["latitude"], quest["longitude"]
        )
        if distance <= radius:
            quest["distance"] = round(distance)
            nearby.append(quest)

    # 거리순 정렬
    nearby.sort(key=lambda x: x["distance"])

    return {"quests": nearby}
