from sqlalchemy import desc, and_
from sqlalchemy.orm import Session
from database import schemas, models


def get_user(db: Session, user_id: int) -> models.User:  # USER
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> models.User:  # USER
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> list:  # USER
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate)-> models.User:  # USER
    db_user = models.User(email=user.email, name=user.name, photo_url=user.photo_url)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100) -> list:  # ITEMS
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, list_id) -> models.Item:  # ITEM
    db_item = models.Item(**item.dict(), owner_list_id=list_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def create_user_list(db: Session, user_list: schemas.UserListCreate, user_id) -> models.UserList:  # LIST
    db_list = models.UserList(title=user_list.title, owner_id=user_id)
    db.add(db_list)
    db.commit()
    db.refresh(db_list)
    return db_list


def get_lists_from_user(db: Session, user_id: int, skip: int = 0, limit: int = 30) -> list:  # LIST
    return db.query(models.UserList).filter(models.UserList.owner_id == user_id).offset(skip).limit(limit).all()


def get_list_by_id(db: Session, list_id: int) -> models.UserList:
    return db.query(models.UserList).filter(models.UserList.id == list_id).first()


def get_items_by_id(db: Session, list_id: int, skip: int = 0, limit: int = 30) -> models.UserList:
    lis = db.query(models.UserList).filter(models.UserList.id == list_id).first()
    lis.items = db.query(models.Item)\
        .order_by(desc(models.Item.id))\
        .filter(and_(models.Item.owner_list_id == list_id,)).offset(skip).limit(limit).all()
    return lis


def get_item_by_id(db: Session, item_id: int) -> models.Item:
    return db.query(models.Item).filter(models.Item.id == item_id).first()


def delete_item_by_id(db: Session, item_id: int) -> bool:
    db.query(models.Item).filter(models.Item.id == item_id).delete()
    db.commit()
    return True


def move_item(db: Session, item_id: int, list_id: int) -> models.Item:
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    item.owner_list_id = list_id
    db.commit()
    return item
