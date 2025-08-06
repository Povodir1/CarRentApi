from schemas import CarFilter,CarBase,Car

from database.tables import session, Cars


def db_get_all_cars(filters:CarFilter):
    with session:
        query = session.query(Cars)
        if filters.brand:
            query = query.filter(Cars.brand == filters.brand)
        if filters.model:
            query = query.filter(Cars.model == filters.model)
        if filters.year:
            query = query.filter(Cars.year == filters.year)
        if filters.body_type:
            query = query.filter(Cars.body_type == filters.body_type)
        if filters.price_per_day:
            query = query.filter(Cars.price_per_day == filters.price_per_day)
        if filters.is_available:
            query = query.filter(Cars.is_available == filters.is_available)
        return query.all()


def db_get_one_car(car_id:int) -> Car:
    with session:
        car = session.query(Cars).filter(Cars.id == car_id).one()
        return car

def db_add_car(new_car: CarBase) -> Car:
    with session:
        added_car = Cars(**new_car.model_dump())
        session.add(added_car)
        session.commit()
        session.refresh(added_car)
        return Car.model_validate(added_car.__dict__)

def db_delete_car(del_car_id:int) -> bool:
    with session:
        car = session.query(Cars).filter(Cars.id == del_car_id).one()
        session.delete(car)
        session.commit()
        return True


def db_update_car(car_id:int,update:CarBase) -> Car:
    with session:
        car = session.query(Cars).filter(Cars.id == car_id).one()
        car.model =update.model
        car.body_type  = update.body_type
        car.brand = update.brand
        car.year = update.year
        car.price_per_day = update.price_per_day
        car.is_available  = update.is_available
        session.commit()
        session.refresh(car)
        return car
