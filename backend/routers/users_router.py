from fastapi import APIRouter, Depends, HTTPException, Form, status
from config.database import conn, get_db
from models.users import Users
from models.reestr import Divisions
from schemas.user_schemas import User, UserCreate

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


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    print("This token is: ", token)
    print("Secret key is:", SECRET_KEY)

    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    email: str = payload.get("email")
    workplace: int = payload.get("workplace")
    department: str = payload.get("department")

    if email is None or workplace is None or department is None:
        print("Email / workplace / department is missing from the token.")
        raise credentials_exception


    user = db.query(Users).filter(Users.email == email).first()

    if user is None:
        raise  credentials_exception
    return user


# REGISTRATION
@user_routers.post('/', tags=["users"])
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = hash_password(user.password)  # Hash the provided password
    workplace_id = db.query(Divisions.division_id).filter(Divisions.division_name == user.workplace).first()

    if not workplace_id:
        raise HTTPException(status_code=400, detail="Workplace not found")

    conn.execute(Users.__table__.insert().values(
        username=user.username,
        lastname=user.lastname, 
        email=user.email, 
        password=hashed_password,  # Store the hashed password
        position=user.position,
        department = user.department,
        workplace = workplace_id[0])
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
    access_token = create_access_token(
        data={
            "email": user.email,
            "workplace": user.workplace,
            "department": user.department  # Добавляем workplace в токен
        }
    )

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

