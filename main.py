from fastapi import FastAPI
from handlers.car import car_router
from handlers.user import user_router
from handlers.booking import booking_router
from fastapi.security import OAuth2PasswordBearer

app = FastAPI(title="CarRentApi")

user_auth = OAuth2PasswordBearer(tokenUrl="/auth/token")

app.include_router(car_router)
app.include_router(user_router)
app.include_router(booking_router)






