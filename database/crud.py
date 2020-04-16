from sqlalchemy.orm import Session
from database import schemas, models


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(email=user.email, name=user.name, photo_url=user.photo_url)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def create_user_list(db: Session, user_list: schemas.UserListCreate, user_id):
    db_list = models.UserList(title=user_list.title, owner_id=user_id)
    db.add(db_list)
    db.commit()
    db.refresh(db_list)
    return db_list


def get_lists_from_user(db: Session, user_id: int, skip: int = 0, limit: int = 30):
    # return db.query(models.UserList).filter(models.UserList.owner_id == user_id).offset
    return db.query(models.UserList).filter(models.UserList.owner_id == user_id).offset(skip).limit(limit).all()
