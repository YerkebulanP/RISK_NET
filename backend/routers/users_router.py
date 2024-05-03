from fastapi import APIRouter, Depends, HTTPException, Form
from config.database import conn, get_db
from models.users import Users
from schemas.schemas import User, UserCreate

from sqlalchemy import select, join, delete
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from config import settings
from datetime import datetime, timedelta
import secrets


from passlib.context import CryptContext
from jose import jwt, JWTError



user_routers = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = secrets.token_urlsafe(32)

def hash_password(password: str):
    return pwd_context.hash(password)
    
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)



# AUTHORIZATION 

# Function to create access token
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt


# REGISTRATION
@user_routers.post('/', tags=["users"])
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = hash_password(user.password)  # Hash the provided password
    conn.execute(Users.__table__.insert().values(
        username=user.username,
        lastname=user.lastname, 
        email=user.email, 
        password=hashed_password,  # Store the hashed password
        position=user.position)
    )
    return conn.execute(select(Users)).fetchall()

# ЛОГИН
# Function to authenticate user
def authenticate_user(db: Session, email: str, password: str):
    user = db.query(Users).filter(Users.email == email).first()
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

@user_routers.post("/login", tags=["users"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401, 
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


    
@user_routers.get('/', tags=["users"])
async def fetch_all_users(): 
    return conn.execute(select(Users)).fetchall()
    
@user_routers.put('/{id}', tags=["users"])
async def update_users(user: User, id: int):
    conn.execute(Users.__table__.update().values(username=user.username, 
                                        lastname=user.lastname, 
                                        email=user.email, 
                                        password=user.password, 
                                        position=user.position)
                .where(Users.id == id)
                )
    return conn.execute(select(Users).where(Users.id == id)).first()


@user_routers.delete('/{id}', tags=["users"])
async def delete_users(id: int):
    conn.execute(delete(Users).where(Users.id == id))

    return conn.execute(select(Users).where(Users.id == id)).first()



# # Change password
# @user_routers.post("/change-password")
# async def change_password(oldPassword: str, newPassword: str):
#     # Здесь добавьте код для проверки старого пароля и обновления нового пароля в базе данных PostgreSQL
#     # Например, вы можете использовать SQLAlchemy для взаимодействия с базой данных
#     # Примерно так:
#     # user = get_user_from_database() # Функция, которая получает пользователя из базы данных
#     # if verify_password(oldPassword, user.password): # Функция, которая проверяет соответствие пароля
#     #     user.password = hash_password(newPassword) # Функция, которая хэширует новый пароль
#     #     update_user_in_database(user) # Функция, которая обновляет пользователя в базе данных
#     #     return {"message": "Password updated successfully"}
#     # else:
#     #     return {"message": "Incorrect old password"}

#     # Здесь нужно подставить соответствующий код для вашей базы данных и логики обновления пароля
#     return {"message": "Password updated successfully"}
    
