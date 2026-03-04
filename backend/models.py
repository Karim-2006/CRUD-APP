from pydantic import BaseModel, Field, BeforeValidator, ConfigDict
from typing import Optional, Annotated

PyObjectId = Annotated[str, BeforeValidator(str)]

class ProductModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str = Field(...)
    description: str = Field(...)
    price: float = Field(...)
    stock: int = Field(...)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "name": "Sample Product",
                "description": "This is a sample product description.",
                "price": 19.99,
                "stock": 100
            }
        }
    )

class UpdateProductModel(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "name": "Sample Product",
                "description": "This is a sample product description.",
                "price": 19.99,
                "stock": 100
            }
        }
    )
