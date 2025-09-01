from pydantic import BaseModel, Field
from datetime import datetime
from typing import Any , Dict

class LeaderboardEntry(BaseModel):
    id: int = Field(..., alias="_id", description="Roblox userId")
    overall_score: int = 0
    weekly_score: int = 0
    monthly_score: int = 0
    level : int = 0
    last_updated: datetime

    class Config:
        allow_population_by_field_name = True  # so you can use 'id' or '_id'
        schema_extra : Dict[str , Dict[str , Any]] = {
            "example": {
                "id": 123456789,
                "overall_score": 5210,
                "weekly_score": 340,
                "monthly_score": 1220,
                "level" : 6,
                "last_updated": "2025-09-01T12:00:00Z"
            }
        }