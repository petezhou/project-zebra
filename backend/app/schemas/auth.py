from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    """Schema for user registration."""

    email: EmailStr
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters")
    full_name: str


class UserLogin(BaseModel):
    """Schema for user login."""

    email: EmailStr
    password: str


class Token(BaseModel):
    """Schema for JWT token response."""

    access_token: str
    token_type: str


class UserResponse(BaseModel):
    """Schema for user responses (no password!)."""

    id: int
    email: str
    full_name: str
    created_at: datetime

    model_config = {"from_attributes": True}
