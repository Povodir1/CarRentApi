from fastapi import APIRouter,Depends,HTTPException
from typing import List

from fastapi.params import Query, Body

from schemas import Car,CarFilter,CarBase
from database.car_db import (db_get_all_cars,
                             db_get_one_car,
                             db_add_car,
                             db_delete_car,
                             db_update_car)
from auth_logic import user_auth,is_admin

car_router = APIRouter(tags=["Cars"])


@car_router.get("/cars",response_model=List[Car])
def get_all_cars(data:CarFilter = Query(None),token: str = Depends(user_auth)):
    if not is_admin(token):
        raise HTTPException(status_code=403, detail="not admin")
    response_data = db_get_all_cars(data)
    if response_data:
        return response_data
    else:
        raise HTTPException(status_code=404,detail="not found")


@car_router.get("/cars/{id}",response_model=Car)
def get_car(car_id:int,token: str = Depends(user_auth)):
    if not is_admin(token):
        raise HTTPException(status_code=403, detail="not admin")
    response_data = db_get_one_car(car_id)
    if response_data:
        return response_data
    else:
        raise HTTPException(status_code=404, detail="not found")



@car_router.post("/cars",response_model=Car,status_code=201)
def add_car(new_car:CarBase,token: str = Depends(user_auth)):
    if not is_admin(token):
        raise HTTPException(status_code=403, detail="not admin")
    response_data = db_add_car(new_car)
    return response_data


@car_router.put("/cars/{id}",response_model=Car)
def update_car(updated_car_id:int,new_data:CarBase = Body(None),token: str = Depends(user_auth)):
    if not is_admin(token):
        raise HTTPException(status_code=403, detail="not admin")
    response_data =  db_update_car(updated_car_id,new_data)
    return response_data


@car_router.delete("/cars/{id}",status_code=204)
def delete_car(del_car_id:int,token: str = Depends(user_auth)):
    if not is_admin(token):
        raise HTTPException(status_code=403, detail="not admin")
    response_data =  db_delete_car(del_car_id)
    if not response_data:
        raise HTTPException(status_code=404, detail="not found")

