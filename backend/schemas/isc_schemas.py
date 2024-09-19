from pydantic import BaseModel
from typing import Optional, List
from datetime import date

# Schemas for BusinessProcess1
class BusinessProcess1Model(BaseModel):
    owner: str
    business_process_1_name: str

class BusinessProcess1Create(BusinessProcess1Model):
    pass

class BusinessProcess1(BusinessProcess1Model):
    business_process_1_id: int

    class Config:
        orm_mode = True

# Schemas for BusinessProcess2
class BusinessProcess2Model(BaseModel):
    business_process_2_name: str
    effect_econ: int
    effect_operational: int
    effect_law: int
    assessment: int
    notes: Optional[str] = None
    business_process_1_id: int

class BusinessProcess2Create(BusinessProcess2Model):
    pass


class BusinessProcess2(BusinessProcess2Model):
    business_process_2_id: int
    average_assessment: float
    business_process_1: BusinessProcess1

    class Config:
        orm_mode = True

# Schema for BOTH business procesess
class BusinessProcessResponse(BaseModel):
    business_process_2_id: int
    business_process_2_name: str
    effect_econ: int
    effect_operational: int
    effect_law: int
    assessment: int
    average_assessment: float
    notes: Optional[str] = None
    business_process_1_id: int
    business_process_1_name: str
    owner: str

# Schemas for RiskMatrix
class RiskMatrixResponse(BaseModel):
    business_process_2_name: str
    business_process_1_name: str
    owner: str
    step_business_process_2_level: str
    step_description: str
    step_performer: str
    risk_code: str
    risk_name: str
    risk_description: Optional[str] = None
    control_procedure_code: Optional[str] = None
    control_procedure_name: Optional[str] = None
    control_procedure_owner: Optional[str] = None
    control_procedure_description: Optional[str] = None
    control_procedure_inner_outer_document: Optional[str] = None
    control_procedure_frequency: Optional[str] = None
    control_procedure_type: Optional[str] = None
    control_procedure_category: Optional[str] = None
    effectivity_assessment: Optional[str] = None
    basis_of_assessment: str
    
class RiskMatrixBase(BaseModel):
    business_process_2_id: int
    business_process_2_name: str
    business_process_1_name: str
    owner: str
    step_business_process_2_level: str
    step_description: str
    step_performer: str
    risk_code: str
    risk_name: str
    risk_description: Optional[str] = None
    control_procedure_code: Optional[str] = None
    control_procedure_name: Optional[str] = None
    control_procedure_owner: Optional[str] = None
    control_procedure_description: Optional[str] = None
    control_procedure_inner_outer_document: Optional[str] = None
    control_procedure_frequency: Optional[str] = None
    control_procedure_type: Optional[str] = None
    control_procedure_category: Optional[str] = None
    effectivity_assessment: Optional[str] = None
    basis_of_assessment: str

class RiskMatrixCreate(RiskMatrixBase):
    pass

class RiskMatrix(RiskMatrixBase):
    risk_matrix_id: int
    business_process_2: BusinessProcess2

    class Config:
        orm_mode = True
        
class PlanScheduleResponse(BaseModel):
    # plan_schedule_id: int
    # business_process_2_id: int
    business_process_2_name: str
    business_process_1_name: str
    owner: str
    block_scheme_update_period_start: date
    block_scheme_update_period_end: date
    control_matrix_update_period_start: date
    control_matrix_update_period_end: date
    control_procedure_assessment_period_start: date
    control_procedure_assessment_period_end: date

    class Config:
        orm_mode = True


# Schemas for PlanSchedule
class PlanScheduleBase(BaseModel):
    business_process_2_id: int
    block_scheme_update_period_start: date
    block_scheme_update_period_end: date
    control_matrix_update_period_start: date
    control_matrix_update_period_end: date
    control_procedure_assessment_period_start: date
    control_procedure_assessment_period_end: date


class PlanScheduleCreate(PlanScheduleBase):
    pass

class PlanSchedule(PlanScheduleBase):
    plan_schedule_id: int
    business_process_2: BusinessProcess2

    class Config:
        orm_mode = True
