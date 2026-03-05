import motor.motor_asyncio
from bson import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_DETAILS = os.getenv("MONGO_DETAILS", "mongodb://localhost:27017")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.products_db

product_collection = database.get_collection("products_collection")
user_collection = database.get_collection("users_collection")

# helpers

def product_helper(product) -> dict:
    return {
        "id": str(product["_id"]),
        "name": product["name"],
        "description": product["description"],
        "price": product["price"],
        "stock": product["stock"],
    }

def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"],
    }

async def retrieve_products():
    products = []
    async for product in product_collection.find():
        products.append(product_helper(product))
    return products

async def add_product(product_data: dict) -> dict:
    product = await product_collection.insert_one(product_data)
    new_product = await product_collection.find_one({"_id": product.inserted_id})
    return product_helper(new_product)

async def retrieve_product(id: str) -> dict:
    product = await product_collection.find_one({"_id": ObjectId(id)})
    if product:
        return product_helper(product)

async def update_product(id: str, data: dict):
    if len(data) < 1:
        return False
    product = await product_collection.find_one({"_id": ObjectId(id)})
    if product:
        updated_product = await product_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_product:
            return True
        return False

async def delete_product(id: str):
    product = await product_collection.find_one({"_id": ObjectId(id)})
    if product:
        await product_collection.delete_one({"_id": ObjectId(id)})
        return True

async def add_user(user_data: dict) -> dict:
    user = await user_collection.insert_one(user_data)
    new_user = await user_collection.find_one({"_id": user.inserted_id})
    return user_helper(new_user)

async def retrieve_user(email: str):
    user = await user_collection.find_one({"email": email})
    return user
