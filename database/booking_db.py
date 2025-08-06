from schemas import BookingBase,BookingGet,Booking
from database.tables import session, Bookings,Cars

def db_bookings(user_id:int):
    with session:
        data = session.query(Bookings).filter(Bookings.user_id == user_id).all()
        return data if data else []

def db_create_booking(booking_data:BookingBase):
    with session:
        days = int((booking_data.end_date - booking_data.start_date).days)
        car_data = session.query(Cars).filter(Cars.id == booking_data.car_id).first()
        price = car_data.price_per_day * days
        if not car_data.is_available:
            return None
        new_booking = Bookings(**booking_data.model_dump(),total_price= price)
        session.add(new_booking)
        car_data.is_available = False
        session.commit()
        session.refresh(new_booking)
        return Booking.model_validate(new_booking.__dict__)


def db_delete_booking(user_id:int,booking_id:int):
    with session:
        data = session.query(Bookings).filter(Bookings.user_id == user_id).filter(Bookings.id == booking_id).one()
        car_id = data.car_id
        car = session.query(Cars).filter(Cars.id == car_id).first()
        car.is_available = True
        session.delete(data)
        session.commit()
        return True

