from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class RegisterResponse(BaseModel):
    id: int
    username: str

    model_config = {"extra": "forbid"}


class AuthResponse(BaseModel):
    accessToken: str
    tokenType: str

    model_config = {"extra": "forbid"}


class CreateItemResponse(BaseModel):
    status: str

    model_config = {"extra": "forbid"}


class ItemStatistics(BaseModel):
    contacts: int
    likes: int
    viewCount: int

    model_config = {"extra": "forbid"}


class GetItemResponse(BaseModel):
    createdAt: datetime
    id: UUID
    name: str
    price: int
    sellerId: int
    statistics: ItemStatistics

    model_config = {"extra": "forbid"}


class StatsResponse(BaseModel):
    contacts: int
    likes: int
    viewCount: int

    model_config = {"extra": "forbid"}
