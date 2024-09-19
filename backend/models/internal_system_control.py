from sqlalchemy import Column, Integer, String, ForeignKey, Float, Date
from sqlalchemy.orm import declarative_base, relationship
from config.database import engine  # Assuming conn is not used in this script

Base = declarative_base()

class Business_process_1(Base):
    __tablename__ = 'business_process_1'
    business_process_1_id = Column(Integer, index=True, autoincrement=True, primary_key=True)
    owner = Column(String, nullable=False)
    business_process_1_name = Column(String, nullable=False)

    business_process_2 = relationship('Business_process_2', back_populates='business_process_1')

class Business_process_2(Base):
    __tablename__ = 'business_process_2'
    business_process_2_id = Column(Integer, index=True, autoincrement=True, primary_key=True)
    business_process_1_id = Column(Integer, ForeignKey('business_process_1.business_process_1_id'))
    business_process_2_name = Column(String, nullable=False)
    effect_econ = Column(Integer, nullable=False)
    effect_operational = Column(Integer, nullable=False)
    effect_law = Column(Integer, nullable=False)
    assessment = Column(Integer, nullable=False)
    average_assessment = Column(Float, nullable=False)
    notes = Column(String)

    business_process_1 = relationship('Business_process_1', back_populates='business_process_2')
    risk_matrix = relationship('Risk_matrix', back_populates='business_process_2')
    plan_schedule = relationship('Plan_schedule', back_populates='business_process_2')

class Risk_matrix(Base):
    __tablename__ = 'risk_matrix'
    risk_matrix_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    business_process_2_id = Column(Integer, ForeignKey('business_process_2.business_process_2_id'))
    step_b_p_2 = Column(String, nullable=False)
    step_description = Column(String, nullable=False)
    step_performer = Column(String, nullable=False)
    risk_code = Column(String, unique=True, nullable=False)
    risk_name = Column(String, unique=True, nullable=False)
    risk_description = Column(String) 
    control_procedure_code = Column(String)
    control_procedure_name = Column(String)
    control_procedure_owner = Column(String)
    control_procedure_description = Column(String)
    control_procedure_inner_outer_document = Column(String)
    control_procedure_frequency = Column(String)
    control_procedure_type = Column(String)
    control_procedure_category = Column(String)
    effectivity_assessment = Column(String)
    basis_of_assessment = Column(String, nullable=False)

    business_process_2 = relationship('Business_process_2', back_populates='risk_matrix')

class Plan_schedule(Base):
    __tablename__ = 'plan_schedule'
    plan_schedule_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    business_process_2_id = Column(Integer, ForeignKey('business_process_2.business_process_2_id'))
    block_scheme_update_period_start = Column(Date, nullable=False)
    block_scheme_update_period_end = Column(Date, nullable=False)
    control_matrix_update_period_start = Column(Date, nullable=False)
    control_matrix_update_period_end = Column(Date, nullable=False)
    control_procedure_assessment_period_start = Column(Date, nullable=False)
    control_procedure_assessment_period_end = Column(Date, nullable=False)

    business_process_2 = relationship('Business_process_2', back_populates='plan_schedule')    

