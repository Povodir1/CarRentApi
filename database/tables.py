from sqlalchemy import Column, Integer, String, Float, Boolean, create_engine, DateTime
from sqlalchemy.orm import declarative_base,Session

from сonfig import settings


engine = create_engine(settings.DB_URL)
session = Session(engine)
Base = declarative_base()

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True)
    name = Column(String(30),nullable=False)
    password = Column(String(),nullable=False)
    email = Column(String(),nullable=False)
    role = Column(String(),nullable = False)

class Cars(Base):
    __tablename__ = "cars"

    id = Column(Integer,primary_key=True)
    brand = Column(String(30),nullable=False)
    model = Column(String(),nullable=False)
    year = Column(Integer,nullable=False)
    price_per_day = Column(Float,nullable = False)
    body_type = Column(String(), nullable=False)
    is_available = Column(Boolean,nullable=False)

class Bookings(Base):
    __tablename__ = "bookings"

    id = Column(Integer,primary_key=True)
    car_id = Column(Integer,nullable=False)
    user_id = Column(Integer,nullable=False)
    start_date = Column(DateTime,nullable=False)
    end_date = Column(DateTime,nullable=False)
    total_price = Column(Float,nullable=False)
