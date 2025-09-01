import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler # type : ignore
from repo.leaderboard_repo import LeaderboardRepository
from datetime import datetime
import calendar

def start_scheduler():
    scheduler = AsyncIOScheduler()

    scheduler.add_job(LeaderboardRepository.reset_weekly, "cron", day_of_week="mon", hour=0, minute=0)

    scheduler.add_job(LeaderboardRepository.reset_monthly, "cron", day=1, hour=0, minute=0)

    scheduler.start()


def get_week() -> int:
    """
    Returns the ISO week number (1–53).
    ISO weeks always start on Monday.
    Handles edge cases like years not starting on Monday.
    """
    return datetime.now().isocalendar().week

def get_month() -> str:
    """
    Returns the full month name (e.g. 'January').
    """
    month_number = datetime.now().month
    return calendar.month_name[month_number]