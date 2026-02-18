from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import os

app = FastAPI()

# --- THE MAGIC SHIELD THAT FIXES YOUR ERROR ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MONGO_URL = os.getenv("MONGO_URL", "mongodb://mongo:27017")
client = AsyncIOMotorClient(MONGO_URL)
db = client.order_db 

class StatusUpdate(BaseModel):
    status: str

@app.post("/update-status/{order_id}")
async def update_status(order_id: str, status: StatusUpdate):
    result = await db.orders.update_one(
        {"_id": ObjectId(order_id)},
        {"$set": {"status": status.status}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"message": "Status updated", "new_status": status.status}

@app.get("/track/{order_id}")
async def track_order(order_id: str):
    try:
        order = await db.orders.find_one({"_id": ObjectId(order_id)})
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return {"order_id": order_id, "status": order.get("status", "UNKNOWN")}
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid Order ID format")