from pydantic import BaseModel, EmailStr, Field

class UserSchema(BaseModel):
    username: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "username": "jdoe",
                "email": "jdoe@example.com",
                "password": "StrongPassword123!"
            }
        }

class UserLoginSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "email": "jdoe@example.com",
                "password": "StrongPassword123!"
            }
        }
