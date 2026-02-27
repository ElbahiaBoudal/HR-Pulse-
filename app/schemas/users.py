from pydantic import BaseModel, EmailStr, Field

class UserRegistre(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, example="admin")
    email: EmailStr = Field(..., example="admin@gmail.com")
    password: str = Field(..., min_length=6, max_length=128, example="admin123")

   

