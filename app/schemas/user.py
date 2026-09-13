from pydantic import BaseModel, EmailStr , Field , ConfigDict
from datetime import datetime
from app.models.users import UserRole


class UserCreate(BaseModel):

    email: EmailStr
    password: str = Field(
        min_length=8,
        max_length=128,
    )

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    role: UserRole
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )