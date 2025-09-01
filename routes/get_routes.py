# app/api/v1/routes/admin_leaderboard.py
from typing import List
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from repo.leaderboard_repo import LeaderboardRepository
from models.leaderboard_entry import LeaderboardEntry
from scheduler import get_week, get_month  # adjust import path if needed
import traceback

class TopListResponse(BaseModel):
    period: str
    top: List[LeaderboardEntry]


router = APIRouter(
    prefix="/leaderboard",
    tags=["Leaderboards"],
)


async def _payload(period_key: str, resp_period: str, limit: int) -> TopListResponse:
    try:
        data = await LeaderboardRepository.get_top(period_key, limit)
        return TopListResponse(period=resp_period, top=data)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to fetch {period_key} leaderboard: {e}")


@router.get("/global", response_model=TopListResponse, summary="Top players (overall/global)")
async def top_global(limit: int = Query(10, ge=1, le=100)):
    # period shown as literal "global"
    return await _payload("overall", "global", limit)


@router.get("/level", response_model=TopListResponse, summary="Top players by level")
async def top_level(limit: int = Query(10, ge=1, le=100)):
    return await _payload("level", "level", limit)


@router.get("/weekly", response_model=TopListResponse, summary="Top players (weekly)")
async def top_weekly(limit: int = Query(10, ge=1, le=100)):
    # use your get_week() helper for the period label
    return await _payload("weekly", str(get_week()), limit)


@router.get("/monthly", response_model=TopListResponse, summary="Top players (monthly)")
async def top_monthly(limit: int = Query(10, ge=1, le=100)):
    # use your get_month() helper for the period label
    return await _payload("monthly", get_month(), limit)
