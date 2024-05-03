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
 
#     position_id = Column(Integer, ForeignKey('position.position_id'), nullable=False)

#     position = relationship('Positions', back_populates='users', cascade="all")


# class Positions(Base):
#     __tablename__  = 'position'
#     position_id = Column(Integer, primary_key= True)
#     position_name = Column(String(100))   

#     users = relationship('Users', back_populates='position', cascade="all")


Base.metadata.create_all(engine)



# users = Table ('users', meta, 
#     Column('id', Integer, primary_key = True),
#     Column('username',String(40), unique = False, nullable = True),
#     Column('email', String(40), unique = False, nullable = True),
#     Column('password', String(256), nullable = False),
#     Column('job_title', String(30), nullable = False),
#     Column('position', String(50))
# )

