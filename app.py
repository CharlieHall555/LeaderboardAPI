from fastapi import FastAPI, Depends, HTTPException, status, Security
from fastapi.security.api_key import APIKeyHeader
from scheduler import start_scheduler
from config import Config


# app.py
from fastapi import FastAPI
from routes.schedule_routes import router as admin_reset_router
from routes.get_routes import router as leaderboard_get_router
from routes.post_routes import router as leaderboard_post_router

API_KEY_NAME = "x-api-key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def require_api_key(api_key: str = Security(api_key_header)):
    if not api_key or api_key != Config.API_KEY:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing API key")

app = FastAPI(
    title="Leaderboard API",
    dependencies=[Depends(require_api_key)]
)

app.include_router(admin_reset_router)
app.include_router(leaderboard_get_router)
app.include_router(leaderboard_post_router)

start_scheduler()


@app.get("/ping")
async def ping():
    return {"message": "pong"}