# app/api/v1/routes/admin_leaderboard.py
from typing import List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from repo.leaderboard_repo import LeaderboardRepository
from models.leaderboard_entry import LeaderboardEntry
import traceback

class UpdateRecord(BaseModel):
    user: int = Field(..., description="Roblox userId")
    new_wins: int = Field(0, description="Delta to apply to weekly/monthly")
    global_wins: int = Field(..., description="Authoritative overall wins (source of truth)")
    level: int = Field(..., description="Authoritative level (source of truth)")

router = APIRouter(
    prefix="/leaderboard",
    tags=["Leaderboards"],
)

@router.post(
    "/update",
    response_model=LeaderboardEntry,
    summary="Update a single player's leaderboard entry",
)
async def update_single(payload: UpdateRecord):
    """
    Applies updates using repository methods only, in this order:
    1) update_score(new_wins)  -> increments weekly/monthly (and overall)
    2) set_level(level)        -> authoritative level
    3) set_global_score(...)   -> authoritative overall (overwrites overall to global_wins)
    """
    try:
        # 1) increment weekly/monthly via existing API (also bumps overall, but we’ll overwrite)
        await LeaderboardRepository.update_score(payload.user, payload.new_wins)

        # 2) set authoritative level
        await LeaderboardRepository.set_level(payload.user, payload.level)

        # 3) set authoritative global/overall (final write so overall is exact)
        final_doc = await LeaderboardRepository.set_global_score(payload.user, payload.global_wins)

        return final_doc

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Update failed: {e}\n{traceback.format_exc()}",
        )

@router.post(
    "/batch",
    response_model=List[LeaderboardEntry],
    summary="Batch update many players",
)
async def update_batch(records: List[UpdateRecord]):
    """
    Loops through records and applies the same 3-step sequence per user using repository methods.
    Returns the final documents (after authoritative set_global_score).
    """
    results: List[LeaderboardEntry] = []
    try:
        for r in records:
            await LeaderboardRepository.update_score(r.user, r.new_wins)
            await LeaderboardRepository.set_level(r.user, r.level)
            final_doc = await LeaderboardRepository.set_global_score(r.user, r.global_wins)
            results.append(final_doc)
        return results

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Batch update failed: {e}\n{traceback.format_exc()}",
        )
