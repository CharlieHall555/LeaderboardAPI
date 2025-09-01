# app/api/v1/routes/admin_leaderboard.py
from fastapi import APIRouter, HTTPException, status, Depends, Security
from fastapi.security.api_key import APIKeyHeader
from repo.leaderboard_repo import LeaderboardRepository
from config import Config
import traceback


router = APIRouter(
    prefix="/reset",
    tags=["reset"],
)

@router.post("/weekly", status_code=status.HTTP_202_ACCEPTED, summary="Force reset weekly leaderboard")
async def force_reset_weekly():
    try:
        await LeaderboardRepository.reset_weekly()
        return {"ok": True, "period": "weekly"}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Weekly reset failed: {e}")

@router.post("/monthly", status_code=status.HTTP_202_ACCEPTED, summary="Force reset monthly leaderboard")
async def force_reset_monthly():
    try:
        await LeaderboardRepository.reset_monthly()
        return {"ok": True, "period": "monthly"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Monthly reset failed: {e}")