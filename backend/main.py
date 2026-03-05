from fastapi import FastAPI, Body, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List

from models.product import ProductModel, UpdateProductModel
from database import (
    add_product,
    delete_product,
    retrieve_product,
    retrieve_products,
    update_product,
    add_user,
    retrieve_user
)
from fastapi.middleware.cors import CORSMiddleware
from auth.utils import get_hashed_password, verify_password, create_access_token, create_refresh_token
from auth.deps import get_current_user
from models.user import UserSchema, UserLoginSchema
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

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
async def delete_product_data(id: str, user: str = Depends(get_current_user)):
    deleted_product = await delete_product(id)
    if deleted_product:
        return JSONResponse(status_code=status.HTTP_200_OK, content="Product deleted successfully")
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"error": "Product not found"})

@app.post("/signup", summary="Create new user")
async def create_user(data: UserSchema):
    # querying database to check if user already exist
    user = await retrieve_user(data.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )
    
    user = {
        "username": data.username,
        "email": data.email,
        "password": get_hashed_password(data.password)
    }
    
    await add_user(user)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "User created successfully"})

@app.post("/login", summary="Create access and refresh tokens for user")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await retrieve_user(form_data.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    hashed_pass = user['password']
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    
    return {
        "access_token": create_access_token(user['email']),
        "refresh_token": create_refresh_token(user['email']),
        "token_type": "bearer"
    }
