from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
import os
from datetime import datetime

app = FastAPI()

# --- CORS CONFIGURATION ---
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

class OrderItem(BaseModel):
    product_id: str
    quantity: int
    price: float

class Order(BaseModel):
    user_id: str
    items: list[OrderItem]
    total: float

@app.post("/order/create")
async def create_order(order: Order):
    order_dict = order.model_dump() # Converts data to dictionary
    order_dict["status"] = "PLACED"
    order_dict["created_at"] = datetime.utcnow()
    
    new_order = await db.orders.insert_one(order_dict)
    return {"order_id": str(new_order.inserted_id), "status": "PLACED"}