from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from database.sql_app import crud, models, schemas
from database.sql_app.database import SessionLocal, engine

from pydantic import BaseModel
import controllers.authentication_controller as auth


"""
Aqui fica a responsabilidade de definir rota e validar as requisições, as demais conecões com o banco e crud fica em 
outro local, (controller e conexao com o banco separado pf)

fastAPI
Restfull
backend
database
"""


class User(BaseModel):
    email: str
    id: int
    name: str
    photo_url: str
    token: str


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


@app.post('/users/', response_model=schemas.User, status_code=201)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail='Email already registered')
    return crud.create_user(db=db, user=user)


@app.get('/users/', response_model=List[schemas.User], status_code=200)
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get('/users/{user_id}', response_model=schemas.User, status_code=200)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return db_user


@app.post('/users/{user_id}/items/', response_model=schemas.Item, status_code=200)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get('/items/', response_model=List[schemas.Item], status_code=200)
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


# codigo antigo
@app.post("/login", status_code=201)
async def login_user(user: User):
    """
    Login and register of users
    :param user:
    :return:
    """
    if not user.email or not user.id or not user.name or not user.token:
        return HTTPException(status_code=400, detail="Bad Request")
    # resp = auth.auth_user(user.token)
    resp = {'auth': True}
    if not resp['auth']:
        # the user wasn't authorized
        return HTTPException(status_code=401, detail="401 Unauthorized")
    # at this point the user was authorized
    return {"message": "Voce chegou à página de registro e criou {} como user".format(user.email)}


@app.get("/", status_code=200)
async def read_root():
    print('acessou o root')
    return {'root': 'hello world'}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None, v: str = None):
    return {"item_id": item_id,
            "q": q,
            "v": v, }
