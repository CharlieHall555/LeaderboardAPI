from config import Config
import motor.motor_asyncio

MONGO_URL = Config.MONGO_URL
DB_NAME = Config.DB_NAME

client  = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL) # type: ignore
db = client[DB_NAME] # type: ignore