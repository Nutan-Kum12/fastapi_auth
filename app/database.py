from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")  # e.g. mongodb+srv://username:password@cluster0.mongodb.net/dbname
client = AsyncIOMotorClient(MONGO_URL)
db = client["auth_db"]
user_collection = db["users"]


