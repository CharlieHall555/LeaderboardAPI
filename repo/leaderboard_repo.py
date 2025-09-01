from typing import List, Optional
from datetime import datetime, timezone
from pymongo import ReturnDocument
from db import db  # type: ignore
from models.leaderboard_entry import LeaderboardEntry


class LeaderboardRepository:
    collection = db["leaderboards"]

    # Map external periods to actual field names
    VALID_SORT_KEYS = {
        "overall": "overall_score",
        "weekly": "weekly_score",
        "monthly": "monthly_score",
        "level": "level",
    }

    @staticmethod
    async def update_score(user_id: int, increment: int,) -> LeaderboardEntry:
        """
        Increment a user's scores (overall, weekly, monthly), and optionally their level.
        """
        now = datetime.now(timezone.utc)
        inc_payload = {
            "overall_score": increment,
            "weekly_score": increment,
            "monthly_score": increment,
        }

        doc = await LeaderboardRepository.collection.find_one_and_update(
            {"_id": user_id},
            {
                "$inc": inc_payload,
                "$set": {"last_updated": now},
                "$setOnInsert": {"level": 0},  # ensure level exists if upserting
            },
            upsert=True,
            return_document=ReturnDocument.AFTER,
        )
        return LeaderboardEntry(**doc)

    @staticmethod
    async def set_level(user_id: int, level: int) -> LeaderboardEntry:
        """Set a user's level explicitly."""
        now = datetime.now(timezone.utc)
        doc = await LeaderboardRepository.collection.find_one_and_update(
            {"_id": user_id},
            {"$set": {"level": level, "last_updated": now}, "$setOnInsert": {
                "overall_score": 0, "weekly_score": 0, "monthly_score": 0
            }},
            upsert=True,
            return_document=ReturnDocument.AFTER,
        )
        return LeaderboardEntry(**doc)

    @staticmethod
    async def increment_level(user_id: int, by: int = 1) -> LeaderboardEntry:
        """Increment a user's level."""
        now = datetime.now(timezone.utc)
        doc = await LeaderboardRepository.collection.find_one_and_update(
            {"_id": user_id},
            {"$inc": {"level": by}, "$set": {"last_updated": now}, "$setOnInsert": {
                "overall_score": 0, "weekly_score": 0, "monthly_score": 0
            }},
            upsert=True,
            return_document=ReturnDocument.AFTER,
        )
        return LeaderboardEntry(**doc)

    @staticmethod
    async def get_by_id(user_id: int) -> Optional[LeaderboardEntry]:
        """Fetch a single user by id."""
        doc = await LeaderboardRepository.collection.find_one({"_id": user_id})
        return LeaderboardEntry(**doc) if doc else None

    @staticmethod
    async def get_top(period: str, limit: int = 10) -> List[LeaderboardEntry]:
        """
        Get top N players by one of: 'overall' | 'weekly' | 'monthly' | 'level'.
        """
        if period not in LeaderboardRepository.VALID_SORT_KEYS:
            raise ValueError("Invalid period. Must be 'overall', 'weekly', 'monthly', or 'level'.")
        field = LeaderboardRepository.VALID_SORT_KEYS[period]
        cursor = LeaderboardRepository.collection.find().sort(field, -1).limit(limit)
        return [LeaderboardEntry(**doc) async for doc in cursor]

    @staticmethod
    async def reset_weekly() -> None:
        """Reset weekly scores to 0."""
        await LeaderboardRepository.collection.update_many({}, {"$set": {"weekly_score": 0}})

    @staticmethod
    async def reset_monthly() -> None:
        """Reset monthly scores to 0."""
        await LeaderboardRepository.collection.update_many({}, {"$set": {"monthly_score": 0}})


    @staticmethod
    async def set_global_score(user_id: int, global_wins: int) -> LeaderboardEntry:
        """
        Set a user's global (overall) score explicitly.
        Use when Roblox server/database is the source of truth.
        """
        now = datetime.now(timezone.utc)
        doc = await LeaderboardRepository.collection.find_one_and_update(
            {"_id": user_id},
            {
                "$set": {
                    "overall_score": global_wins,
                    "last_updated": now,
                },
                "$setOnInsert": {
                    "weekly_score": 0,
                    "monthly_score": 0,
                    "level": 0,
                },
            },
            upsert=True,
            return_document=ReturnDocument.AFTER,
        )
        return LeaderboardEntry(**doc)