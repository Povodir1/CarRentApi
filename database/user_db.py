from schemas import UserUpdate,UserCreate,UserLogin,User

from auth_logic import hash_pass,verify_pass
from database.tables import Users,session

def db_user_register(new_user:UserCreate) -> dict:
    with session:
        new_user.password = hash_pass(new_user.password)
        user_data = new_user.model_dump()
        user_data.update({
            'role': 'user'
        })
        user = Users(**user_data)
        session.add(user)
        session.commit()
        return {"id":user.id,"role":user.role}

def db_user_login(login_user:UserLogin):
    with session:
        user = session.query(Users).filter(Users.name == login_user.name).one()
        if verify_pass(login_user.password, user.password):
            return {"id":user.id,"role":user.role}
        else:
            return None

def db_user_info(user_id:int):
    with session:
        user = session.query(Users).filter(Users.id == user_id).one()
        return User(id=user.id,name=user.name,email=user.email,role=user.role)


def db_user_update(user_id:int, new_data:UserUpdate):
    with session:
        user = session.query(Users).filter(Users.id == user_id).one()
        user.name = new_data.name
        user.email = new_data.email
        session.commit()
        return user
