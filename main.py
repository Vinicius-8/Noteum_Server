from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

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
    password: str


app = FastAPI()


def response_db():
    """
    Funcção que pertence a um controller
    :return:
    """
    return {'dabatase': 'database_name_connecion'}


@app.post("/register", status_code=201)
async def register_user(user: User):
    if not user.password or not user.email:
        return HTTPException(status_code=400, detail="Missing data")
    return {"message": "Voce chegou à página de registro e criou {} como user".format(user.email)}


@app.get("/", status_code=200)
async def read_root():
    print('acessou o root')
    return response_db()


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None, v: str = None):
    return {"item_id": item_id,
            "q": q,
            "v": v, }
