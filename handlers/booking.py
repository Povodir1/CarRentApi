from fastapi import APIRouter,Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer
from typing import List
from datetime import date
from schemas import BookingBase,Booking
from database.booking_db import db_create_booking,db_bookings,db_delete_booking
from auth_logic import decode_token

booking_router = APIRouter(tags = ["Booking"])

user_auth = OAuth2PasswordBearer(tokenUrl="/auth/token")

@booking_router.post("/bookings",response_model=Booking)
def create_booking(car_id:int,
                   start_date:date,
                   end_date:date,
                    token:str = Depends(user_auth)):
    user_id  = decode_token(token).get("id")
    response_data = db_create_booking(BookingBase(car_id=car_id, user_id=user_id, start_date=start_date, end_date=end_date))
    if response_data:
        return response_data
    else:
        raise HTTPException(status_code=400, detail="invalid query")


@booking_router.get("/bookings",response_model=List[Booking])
def get_bookings(token:str = Depends(user_auth)):
    user_id = decode_token(token).get("id")
    response_data = db_bookings(user_id)
    return response_data


@booking_router.delete("/bookings/{booking_id}",status_code=204)
def del_booking(booking_id:int,token:str = Depends(user_auth)):
    user_id = decode_token(token).get("id")
    response_data = db_delete_booking(user_id,booking_id)
    if not response_data:
        raise HTTPException(status_code = 404)