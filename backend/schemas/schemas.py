from pydantic import BaseModel
from typing import Optional, List

# Схемы для пользователей
class UserBase(BaseModel):
    username: str
    lastname: str
    email: str
    password: str
    position: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

# Схемы для категорий рисков
class RiskCategoryBase(BaseModel):
    risk_code: str
    risk_category_name: str
    description: str

class RiskCategory(RiskCategoryBase):
    class Config:
        orm_mode = True

# Схемы для факторов риска уровня 1
class RiskFactor1Base(BaseModel):
    description_1: str
    owner: str
    control_sp: str
    priority: str = None
    risk_code: str

class RiskFactor1Create(RiskFactor1Base):
    pass

class RiskFactor1(RiskFactor1Base):
    level_1_id: str

    class Config:
        orm_mode = True

# Схемы для факторов риска уровня 2
class RiskFactor2Base(BaseModel):
    description_2: str
    datatype: str
    prob: float
    effect: float
    comments: str
    swot: str
    level_1_id: str

class RiskFactor2Create(RiskFactor2Base):
    pass

class RiskFactor2(RiskFactor2Base):
    level_2_id: str

    class Config:
        orm_mode = True

# Схемы для событий факторов риска уровня 2
class RiskFactor2EventBase(BaseModel):    
    # event_id: int
    event_name: str
    responsible_sp: str
    event_effectiveness: str

class RiskFactor2EventCreate(RiskFactor2EventBase):
    pass

class RiskFactor2Event(RiskFactor2EventBase):
    level_2_id: str

    class Config:
        orm_mode = True

# Схемы для факторов риска уровня 3
class RiskFactor3Base(BaseModel):
    description_3: str
    datatype: str
    prob: float
    effect: float
    comments: str
    level_2_id: str

class RiskFactor3Create(RiskFactor3Base):
    pass

class RiskFactor3(RiskFactor3Base):
    level_3_id: str

    class Config:
        orm_mode = True

# Схемы для факторов риска уровня 4
class RiskFactor4Base(BaseModel):
    description_4: str
    datatype: str
    prob: float
    effect: float
    comments: str
    level_3_id: str

class RiskFactor4Create(RiskFactor4Base):
    pass

class RiskFactor4(RiskFactor4Base):
    level_4_id: str

    class Config:
        orm_mode = True
