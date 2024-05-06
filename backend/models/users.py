from config.database import conn, engine
from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean, Table
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


class Users(Base):
    __tablename__ = 'users' 
    id = Column(Integer, primary_key = True)
    username = Column(String(40), unique = False, nullable = False)
    lastname = Column(String(40), unique = False, nullable = False)
    email = Column(String(40), unique = False, nullable = False)
    password = Column(String(256), nullable = False)
    position = Column(String(100))   


Base.metadata.create_all(engine)

