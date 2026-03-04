from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List

from models import ProductModel, UpdateProductModel
from database import (
    add_product,
    delete_product,
    retrieve_product,
    retrieve_products,
    update_product,
)
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/product", response_description="Product data added into the database")
async def add_product_data(product: ProductModel = Body(...)):
    product = jsonable_encoder(product)
    # Remove _id if it's None so MongoDB generates it
    if "_id" in product and product["_id"] is None:
        del product["_id"]
    new_product = await add_product(product)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=new_product)

@app.get("/products", response_description="Products retrieved")
async def get_products():
    products = await retrieve_products()
    if products:
        return JSONResponse(status_code=status.HTTP_200_OK, content=products)
    return JSONResponse(status_code=status.HTTP_200_OK, content=[])


@app.get("/product/{id}", response_description="Product data retrieved")
async def get_product_data(id: str):
    product = await retrieve_product(id)
    if product:
        return JSONResponse(status_code=status.HTTP_200_OK, content=product)
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"error": "Product not found"})

@app.put("/product/{id}")
async def update_product_data(id: str, req: UpdateProductModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_product = await update_product(id, req)
    if updated_product:
        return JSONResponse(status_code=status.HTTP_200_OK, content="Product updated successfully")
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"error": "Product not found"})

@app.delete("/product/{id}", response_description="Product data deleted from the database")
async def delete_product_data(id: str):
    deleted_product = await delete_product(id)
    if deleted_product:
        return JSONResponse(status_code=status.HTTP_200_OK, content="Product deleted successfully")
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"error": "Product not found"})
