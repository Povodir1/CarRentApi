from fastapi import APIRouter,Depends,HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from schemas import User,UserUpdate,UserCreate,UserLogin

from database.user_db import db_user_register,db_user_info,db_user_update,db_user_login

from auth_logic import create_token,decode_token,user_auth

user_router = APIRouter(tags=["Users"])





@user_router.post("/auth/token")
def token_def(form_data: OAuth2PasswordRequestForm = Depends()):
    user_data = db_user_login(UserLogin(name=form_data.username,password=form_data.password))
    if user_data:
        token = create_token(user_data)
        return {"access_token": token,
                "token_type": "bearer"}
    else:
        raise HTTPException(status_code = 404,detail="no found user")



@user_router.post("/auth/register",status_code=201)
def user_register(new_user: UserCreate):
    user_data = db_user_register(new_user)
    token = create_token(user_data)
    return  {"access_token": token,
             "token_type": "bearer"}


@user_router.post("/auth/login")
async def user_login(form_data: UserLogin):
    user_data = db_user_login(form_data)
    if user_data:
        token = create_token(user_data)
        return {"access_token": token,
                "token_type": "bearer"}
    else:
        raise HTTPException(status_code = 404,detail="no found user")



@user_router.get("/user/me",response_model=User)
def user_info(token: str = Depends(user_auth)):
    payload = decode_token(token)
    user_id = payload.get("id")
    response_data = db_user_info(user_id)
    if response_data:
        return response_data
    else:
        raise HTTPException(status_code = 404,detail="no found user")


@user_router.put("/user/me",response_model=User)
def user_update(data:UserUpdate,token: str = Depends(user_auth)):
    payload = decode_token(token)
    user_id = payload.get("id")
    response_data = db_user_update(user_id,data)
    if response_data:
        return response_data
    else:
        raise HTTPException(status_code = 404,detail="no found user")