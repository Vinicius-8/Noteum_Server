from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    photo_url = Column(String)
    lists = relationship('UserList', back_populates='owner')


class UserList(Base):
    __tablename__ = 'user_lists'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship('User', backref='owner')


class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    img_url = Column(String)
    url = Column(String)
    owner_list_id = Column(Integer, ForeignKey('user_lists.id'))
    # owner = relationship('UserList', backref='items')

