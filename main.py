from typing import List

from fastapi import Depends, FastAPI, HTTPException, Header, status

from sqlalchemy.orm import Session

from database import crud
from database import schemas, models
from database.database import SessionLocal, engine

import controllers.authentication_controller as auth

from pydantic import BaseModel

"""
Aqui fica a responsabilidade de definir rota e validar as requisições, as demais conecões com o banco e crud fica em 
outro local, (controller e conexao com o banco separado pf)

fastAPI
Restfull
backend
database
"""

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

# criando uma dependencia para o banco de dados que será usado em apenas um request e depois será
# fechado. Ou seja uma sessão indepedente para o banco por request, que será usada durante
# tod.o o request e depois fechada com a finalização desse request


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.post('/users', response_model=schemas.User, status_code=201)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    token_validated = auth.auth_token(user.token)
    if not token_validated['auth']:  # token not valid
        return HTTPException(status_code=401, detail="401 Unauthorized")
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:  # email already created
        print('o usuario foi autorizado -----')
        raise HTTPException(status_code=status.HTTP_202_ACCEPTED, detail='ACCEPTED')
    return crud.create_user(db=db, user=user)  # creation


# GET | read the user by id
@app.get('/users', response_model=schemas.User, status_code=200)
def read_user(db: Session = Depends(get_db), user_id: int = Header(None)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return db_user

# POST | user list creator route
@app.post('/lists', response_model=schemas.UserList, status_code=200)
def create_list_for_user(user_list: schemas.UserListCreate, db: Session = Depends(get_db), user_id: int = Header(None)):
    return crud.create_user_list(db, user_list, user_id)


# GET | user list reader
@app.get('/lists', response_model=List[schemas.UserList], status_code=200)
def read_lists_from_user(user_id: int = Header(None), skip: int = 0, limit: int = 30, db: Session = Depends(get_db)):
    lists = crud.get_lists_from_user(db, user_id, skip, limit)
    return lists

# create_list_for_user(user_list: schemas.UserListCreate, db: Session = Depends(get_db), user_id: int = Header(None)):
@app.post('/items', response_model=schemas.Item, status_code=200)
def create_item_for_list(
        items: schemas.ItemCreate, db: Session = Depends(get_db),
        owner_id: int = Header(None), owner_list_id: int = Header(None)):
    res = crud.get_list_by_id(db, owner_list_id)
    if owner_id != res.owner_id:
        raise HTTPException(status_code=401, detail='Unauthorized')
    return crud.create_user_item(db, items, owner_id)


@app.post("/login", status_code=status.HTTP_200_OK)
async def login_user(login: schemas.Login):
    print('acessou o root')
    token_validated = auth.auth_token(login.token)
    if not token_validated['auth']:  # token not valid
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="401 Unauthorized")
    return {'root': 'hello world'}
