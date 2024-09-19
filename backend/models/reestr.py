from config.database import conn, engine
from sqlalchemy import Column, Integer, String, ForeignKey, text, Boolean, Table, Float, case
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class RiskCategory(Base):
    __tablename__ = 'risk_category'
    risk_code = Column(String, primary_key=True)
    risk_category_name = Column(String)
    description = Column(String)

class Divisions(Base):
    __tablename__ = 'structure_divisions'
    division_id = Column(Integer, primary_key=True)
    division_name = Column(String)
    shortened_name = Column(String)
    
    risk_factor_1 =  relationship('RiskFactor1', back_populates='division')

class RiskFactor1(Base):
    __tablename__ = 'risk_factor_1'

    level_1_id = Column(String, primary_key=True)
    division_id = Column(Integer, ForeignKey("structure_divisions.division_id"))

    description_1 = Column(String)
    owner = Column(String)
    control_sp = Column(String)
    total_prob = Column(Float)
    total_effect = Column(Float)
    total_loss = Column(Float)  
    priority = Column(String, nullable=True)
    
    division = relationship("Divisions", back_populates="risk_factor_1")

    risk_code = Column(String, ForeignKey('risk_category.risk_code'))


class RiskFactor2(Base):
    __tablename__ = 'risk_factor_2'

    level_2_id = Column(String, primary_key=True)

    description_2 = Column(String)

    # Количественные и качественные
    datatype = Column(String)
    prob = Column(Float)
    effect = Column(Float)
    loss = Column(Float) # Calculated by prob and effect
    comments = Column(String)
    residual_loss = Column(Float)
    swot = Column(String)

    level_1_id = Column(String, ForeignKey('risk_factor_1.level_1_id'))

    events = relationship('RiskFactor2Event', back_populates='risk_factor_2')

class RiskFactor3(Base):
    __tablename__ = 'risk_factor_3'

    level_3_id = Column(String, primary_key=True)
    description_3 = Column(String)
    
    datatype = Column(String)
    prob = Column(Float)
    effect = Column(Float)
    loss = Column(Float)
    comments = Column(String)
    residual_loss = Column(Float)

    level_2_id = Column(String, ForeignKey('risk_factor_2.level_2_id'))


class RiskFactor4(Base):
    __tablename__ = 'risk_factor_4'

    level_4_id = Column(String, primary_key=True)
    description_4 = Column(String)

    datatype = Column(String)
    prob = Column(Float)
    effect = Column(Float)
    loss = Column(Float)
    comments = Column(String)
    residual_loss = Column(Float)

    level_3_id = Column(String, ForeignKey('risk_factor_3.level_3_id'))

class RiskFactor2Event(Base):
    __tablename__ = 'risk_factor_2_event'

    event_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    event_name = Column(String)
    responsible_sp = Column(String)
    event_effectiveness = Column(String)

    level_2_id = Column(String, ForeignKey('risk_factor_2.level_2_id'))
    
    risk_factor_2 = relationship('RiskFactor2', back_populates='events')

RiskFactor1.children = relationship('RiskFactor2', order_by=RiskFactor2.level_2_id, back_populates='parent')
RiskFactor2.children = relationship('RiskFactor3', order_by=RiskFactor3.level_3_id, back_populates='parent')
RiskFactor3.children = relationship('RiskFactor4', order_by=RiskFactor4.level_4_id, back_populates='parent')

RiskFactor2.parent = relationship('RiskFactor1', back_populates='children')
RiskFactor3.parent = relationship('RiskFactor2', back_populates='children')
RiskFactor4.parent = relationship('RiskFactor3', back_populates='children')

Base.metadata.create_all(engine)