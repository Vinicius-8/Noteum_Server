from typing import List
from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: str
    img_url: str


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str
    name: str
    photo_url: str


class UserCreate(UserBase):
    token: str


class User(UserBase):
    id: int
    items: List[Item] = []

    class Config:
        orm_mode = True
