from typing import List
from pydantic import BaseModel


class Login(BaseModel):
    email: str
    token: str


class ItemBase(BaseModel):  # Item
    title: str
    description: str
    img_url: str


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_list_id: int

    class Config:
        orm_mode = True


class UserListBase(BaseModel):  # UserList
    title: str


class UserListCreate(UserListBase):
    pass


class UserList(UserListBase):
    id: int
    items: List[Item] = []
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):  # User
    email: str
    name: str
    photo_url: str


class UserCreate(UserBase):
    token: str


class User(UserBase):
    id: int
    lists: List[UserList] = []

    class Config:
        orm_mode = True
