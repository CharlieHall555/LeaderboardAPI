import os
from dotenv import load_dotenv

load_dotenv()  # reads .env file automatically

class Config:
    API_KEY = os.getenv("API_KEY")
    MONGO_URL = os.getenv("MONGO_URL")
    DB_NAME = os.getenv("DB_NAME")