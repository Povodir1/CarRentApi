from pydantic import BaseModel, Field,EmailStr
from datetime import date
from typing import Optional

class CarBase(BaseModel):
    brand: str
    model: str
    year: int = Field(gt=1800,lt=2026)
    price_per_day: float
    body_type: str
    is_available: bool

class UserBase(BaseModel):
    name: str
    email: EmailStr

class BookingBase(BaseModel):
    car_id: int
    user_id: int
    start_date: date
    end_date: date

class BookingGet(BookingBase):
    total_price: float

class UserCreate(UserBase):
    password: str = Field(min_length= 8)

class Car(CarBase):
    id: int

class User(UserBase):
    id: int
    role: str

class Booking(BookingGet):
    id: int


class CarFilter(BaseModel):
    brand: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    price_per_day: Optional[int] = None
    body_type: Optional[str] = None
    is_available: Optional[bool] = None

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None


class UserLogin(BaseModel):
    name:str
    password: str

