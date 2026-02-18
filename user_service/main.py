from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
import os

app = FastAPI()

# Database Connection
MONGO_URL = os.getenv("MONGO_URL", "mongodb://mongo:27017")
client = AsyncIOMotorClient(MONGO_URL)
db = client.user_db

class User(BaseModel):
    email: str
    password: str
    name: str = "User"

@app.post("/register")
async def register(user: User):
    existing_user = await db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="User exists")
    # In real app, hash password here
    await db.users.insert_one(user.dict())
    return {"message": "User created", "user_id": str(user.email)}

@app.post("/login")
async def login(user: User):
    # Simple password check (plaintext for assignment scope)
    record = await db.users.find_one({"email": user.email, "password": user.password})
    if not record:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"token": "dummy_token_123", "user_id": str(record["email"])}

@app.get("/profile/{user_id}")
async def get_profile(user_id: str):
    user = await db.users.find_one({"email": user_id})
    if user:
        user["_id"] = str(user["_id"])
        return user
    raise HTTPException(status_code=404, detail="User not found")