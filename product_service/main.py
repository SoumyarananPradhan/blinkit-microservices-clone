from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # <-- NEW IMPORT
from motor.motor_asyncio import AsyncIOMotorClient
import os

app = FastAPI()

# --- NEW CORS CONFIGURATION ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows requests from your Flutter Web app
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ------------------------------

MONGO_URL = os.getenv("MONGO_URL", "mongodb://mongo:27017")
client = AsyncIOMotorClient(MONGO_URL)
db = client.product_db

@app.get("/products")
async def get_products():
    products = await db.products.find().to_list(100)
    for p in products:
        p["_id"] = str(p["_id"])
    return products

@app.get("/seed")
async def seed_data():
    # Helper to populate DB quickly
    if await db.products.count_documents({}) == 0:
        sample_products = [
            {"name": "Milk", "price": 50, "category": "Dairy", "image": "https://via.placeholder.com/150"},
            {"name": "Bread", "price": 40, "category": "Bakery", "image": "https://via.placeholder.com/150"},
            {"name": "Eggs", "price": 70, "category": "Dairy", "image": "https://via.placeholder.com/150"},
            {"name": "Chips", "price": 20, "category": "Snacks", "image": "https://via.placeholder.com/150"}
        ]
        await db.products.insert_many(sample_products)
        return {"message": "Database seeded!"}
    return {"message": "Database already has data"}