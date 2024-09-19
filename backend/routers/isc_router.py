from fastapi import APIRouter, Depends, HTTPException, Form, Path, Query 
from config.database import conn, get_db
from sqlalchemy.orm import Session, joinedload, contains_eager
from typing import Optional, List, Union
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, update, func, Integer, cast, String
from sqlalchemy.sql import text

from schemas.isc_schemas import (BusinessProcess1, BusinessProcess1Create, BusinessProcess2, BusinessProcess2Create, BusinessProcessResponse, 
                                PlanSchedule, PlanScheduleCreate, PlanScheduleResponse, 
                                RiskMatrix, RiskMatrixCreate, RiskMatrixResponse)

from models.internal_system_control import Business_process_1, Business_process_2, Plan_schedule, Risk_matrix

isc_routers = APIRouter()


# GET METHODS

# get business process 1 level
@isc_routers.get("/internal_system_control/business_process_1/", response_model=List[BusinessProcess1], tags=['internal_system_control'])
def get_business_process_1(db: Session = Depends(get_db)):
    business_process_1 = db.query(Business_process_1).all()
    return business_process_1

# @isc_routers.get("/internal_system_control/business_process_2/", response_model=List[BusinessProcessResponse], tags=['internal_system_control'])
# def get_all_business_process(db: Session = Depends(get_db)):
#     isc = db.query(Business_process_2).options(joinedload(Business_process_2.business_process_1)).all()

#     result = []
#     for bp2 in isc:
#         data = {
#             "business_process_1_id": bp2.business_process_1.business_process_1_id,
#             "business_process_2_id": bp2.business_process_2_id,
#             "business_process_1_name": bp2.business_process_1.business_process_1_name if bp2.business_process_1 else None,
#             "business_process_2_name": bp2.business_process_2_name,
#             "owner": bp2.business_process_1.owner,
#             "effect_econ": bp2.effect_econ,
#             "effect_operational": bp2.effect_operational,
#             "effect_law": bp2.effect_law,
#             "assessment": bp2.assessment,
#             "average_assessment": bp2.average_assessment,
#             "notes": bp2.notes
#         }
#         result.append(data)

    return result

@isc_routers.get("/internal_system_control/business_process_2/{business_process_1_id}", response_model=list, tags=['internal_system_control'])
def get_business_process_2_by_1_level(business_process_1_id: int, db: Session = Depends(get_db)):
    business_process_2_descriptions = (
        db.query(Business_process_2)
        .join(Business_process_1, Business_process_1.business_process_1_id == Business_process_2.business_process_1_id)
        .filter(Business_process_1.business_process_1_id == business_process_1_id).all()
     )

    descriptions = [{"business_process_2_id": item.business_process_2_id, "business_process_2_name": item.business_process_2_name} 
                    for item in business_process_2_descriptions]

    return descriptions
     
# Get block-scheme
@isc_routers.get("/internal_system_control/get/plan_schedule/", response_model=List[PlanScheduleResponse], tags=['internal_system_control'])
def get_block_scheme(db: Session = Depends(get_db)):
    isc_bs = (
        db.query(
            Plan_schedule,
            Business_process_2.business_process_2_id,
            Business_process_1.business_process_1_name,
            Business_process_2.business_process_2_name,
            Business_process_1.owner
        )
        .join(Plan_schedule.business_process_2)
        .join(Business_process_2.business_process_1)
        .options(
            joinedload(Plan_schedule.business_process_2).joinedload(Business_process_2.business_process_1)
        )
        .all()
    )

    results = []

    for ps, bp2_id, bp1_name, bp2_name, owner in isc_bs:
        data = {
            "business_process_2_id": bp2_id,
            "business_process_1_name": bp1_name,
            "business_process_2_name": bp2_name,
            "owner": owner,
            "block_scheme_update_period_start": ps.block_scheme_update_period_start,
            "block_scheme_update_period_end": ps.block_scheme_update_period_end,
            "control_matrix_update_period_start": ps.control_matrix_update_period_start,
            "control_matrix_update_period_end": ps.control_matrix_update_period_end,
            "control_procedure_assessment_period_start": ps.control_procedure_assessment_period_start,
            "control_procedure_assessment_period_end": ps.control_procedure_assessment_period_end
        }
        print(data)
        results.append(data)

    return results

# Get Risk Matrix
@isc_routers.get("/internal_system_control/get/risk_matrix/", response_model=List[RiskMatrixResponse], tags=['internal_system_control'])
def get_risk_matrix(db: Session = Depends(get_db)):
    isc_bs = (
        db.query(
            Risk_matrix,
            Business_process_2.business_process_2_id,
            Business_process_1.business_process_1_name,
            Business_process_2.business_process_2_name,
            Business_process_1.owner
        )
        .join(Risk_matrix.business_process_2)
        .join(Business_process_2.business_process_1)
        .options(
            joinedload(Risk_matrix.business_process_2).joinedload(Business_process_2.business_process_1)
        )
        .all()
    )

    results = []

    for ps, bp2_id, bp1_name, bp2_name, owner in isc_bs:
        data = {
            "business_process_2_id": bp2_id,
            "business_process_1_name": bp1_name,
            "business_process_2_name": bp2_name,
            "owner": owner,
            "step_business_process_2_level": ps.step_b_p_2,
            "step_description": ps.step_description,
            "step_performer":ps.step_performer,
            "risk_code": ps.risk_code,
            "risk_name":ps.risk_name,
            "risk_description": ps.risk_description,
            "control_procedure_code": ps.control_procedure_code,
            "control_procedure_name": ps.control_procedure_name,
            "control_procedure_owner": ps.control_procedure_owner,
            "control_procedure_description": ps.control_procedure_description,
            "control_procedure_inner_outer_document": ps.control_procedure_inner_outer_document,
            "control_procedure_frequency": ps.control_procedure_frequency,
            "control_procedure_type": ps.control_procedure_type,
            "control_procedure_category": ps.control_procedure_category,
            "effectivity_assessment": ps.effectivity_assessment,
            "basis_of_assessment": ps.basis_of_assessment,
        }

        print(data)
        results.append(data)

    return results

# POST METHODS 

# create business process 1 level
@isc_routers.post("/internal_system_control/post/business_process_1/", response_model=BusinessProcess1, tags=['internal_system_control'])
def create_business_process_1(business_process_1: BusinessProcess1Create ,db: Session = Depends(get_db)):
    db_business_process_1 = Business_process_1(
        owner=business_process_1.owner,
        business_process_1_name=business_process_1.business_process_1_name
    )
    db.add(db_business_process_1)
    db.commit()
    db.refresh(db_business_process_1)
    return db_business_process_1


# create business process 2 level via business process 1
@isc_routers.post("/internal_system_control/post/business_process_2/", response_model=BusinessProcess2, tags=["internal_system_control"])
def create_business_process_2(business_process_2: BusinessProcess2Create, db: Session = Depends(get_db)):
    average_assessment = (business_process_2.effect_econ + business_process_2.effect_operational + business_process_2.effect_law + business_process_2.assessment) / 4

    db_business_process_2 = Business_process_2(
        business_process_2_name = business_process_2.business_process_2_name,
        effect_econ = business_process_2.effect_econ,
        effect_operational = business_process_2.effect_operational,
        effect_law = business_process_2.effect_law,
        assessment = business_process_2.assessment,
        average_assessment = average_assessment,
        notes = business_process_2.notes,
        business_process_1_id = business_process_2.business_process_1_id
    )

    db.add(db_business_process_2)
    db.commit()
    db.refresh(db_business_process_2)
    return db_business_process_2

# create plan_schedule

@isc_routers.post("/internal_system_control/post/plan_schedule/", response_model=PlanScheduleResponse, tags=['internal_system_control'])
def create_plan_schedule(plan_schedule: PlanScheduleCreate, db: Session = Depends(get_db)):
    # Create new Plan_schedule instance
    db_plan_schedule = Plan_schedule(
        business_process_2_id=plan_schedule.business_process_2_id,
        block_scheme_update_period_start=plan_schedule.block_scheme_update_period_start,
        block_scheme_update_period_end=plan_schedule.block_scheme_update_period_end,
        control_matrix_update_period_start=plan_schedule.control_matrix_update_period_start,
        control_matrix_update_period_end=plan_schedule.control_matrix_update_period_end,
        control_procedure_assessment_period_start=plan_schedule.control_procedure_assessment_period_start,
        control_procedure_assessment_period_end=plan_schedule.control_procedure_assessment_period_end,
    )

    db.add(db_plan_schedule)
    db.commit()
    db.refresh(db_plan_schedule)

    # Fetch related BusinessProcess2 data
    business_process_2_data = (
        db.query(Business_process_2, Business_process_1)
        .join(Business_process_1, Business_process_2.business_process_1_id == Business_process_1.business_process_1_id)
        .filter(Business_process_2.business_process_2_id == db_plan_schedule.business_process_2_id)
        .first()
    )
    
    # Create response data including user input and related business process information

    if business_process_2_data:
        business_process_2, business_process_1 = business_process_2_data

        response_data = PlanScheduleResponse(
            business_process_2_id=db_plan_schedule.business_process_2_id,
            business_process_2_name=business_process_2.business_process_2_name,
            block_scheme_update_period_start=db_plan_schedule.block_scheme_update_period_start,
            block_scheme_update_period_end=db_plan_schedule.block_scheme_update_period_end,
            control_matrix_update_period_start=db_plan_schedule.control_matrix_update_period_start,
            control_matrix_update_period_end=db_plan_schedule.control_matrix_update_period_end,
            control_procedure_assessment_period_start=db_plan_schedule.control_procedure_assessment_period_start,
            control_procedure_assessment_period_end=db_plan_schedule.control_procedure_assessment_period_end,
            business_process_1_name=business_process_1.business_process_1_name,
            owner=business_process_1.owner,
        )

    else:
        raise HTTPException(status_code=404, detail="BusinessProcess2 not found")

    return response_data

    # if business_process_2_data:
    #     business_process_1_data = db.query(Business_process_1).filter(Business_process_1.business_process_1_id == business_process_2_data.business_process_1_id).first()

    # # Create response data
    # if business_process_2_data:
    #     response_data = PlanScheduleResponse(
    #         business_process_2_id=db_plan_schedule.business_process_2_id,
    #         business_process_2_name=business_process_2_data.business_process_2_name,
    #         block_scheme_update_period_start=db_plan_schedule.block_scheme_update_period_start,
    #         block_scheme_update_period_end=db_plan_schedule.block_scheme_update_period_end,
    #         control_matrix_update_period_start=db_plan_schedule.control_matrix_update_period_start,
    #         control_matrix_update_period_end=db_plan_schedule.control_matrix_update_period_end,
    #         control_procedure_assessment_period_start=db_plan_schedule.control_procedure_assessment_period_start,
    #         control_procedure_assessment_period_end=db_plan_schedule.control_procedure_assessment_period_end,

    #         business_process_1_name=business_process_2_data.business_process_1.business_process_1_name,
    #         owner=business_process_2_data.business_process_1.owner,
    #     )

    # else:
    #     raise HTTPException(status_code=404, detail="BusinessProcess2 not found")

    # return response_data

@isc_routers.post("/internal_system_control/post/risk_matrix/", response_model = RiskMatrixResponse, tags=['internal_system_control'])
def create_risk_matrix(risk_matrix: RiskMatrixCreate, db: Session = Depends(get_db)):
    db_risk_matrix = Risk_matrix(
        business_process_2_id = risk_matrix.business_process_2_id,
        step_b_p_2 = risk_matrix.step_business_process_2_level,
        step_description = risk_matrix.step_description,
        step_performer = risk_matrix.step_performer,
        risk_code = risk_matrix.risk_code,
        risk_name = risk_matrix.risk_name,
        risk_description = risk_matrix.risk_description,
        control_procedure_code = risk_matrix.control_procedure_code,                       
        control_procedure_name = risk_matrix.control_procedure_name,
        control_procedure_owner = risk_matrix.control_procedure_owner,     
        control_procedure_description = risk_matrix.control_procedure_description,       
        control_procedure_inner_outer_document = risk_matrix.control_procedure_inner_outer_document,
        control_procedure_frequency = risk_matrix.control_procedure_frequency,              
        control_procedure_type = risk_matrix.control_procedure_type,       
        control_procedure_category = risk_matrix.control_procedure_category,      
        effectivity_assessment = risk_matrix.effectivity_assessment,
        basis_of_assessment = risk_matrix.basis_of_assessment 

    )

    db.add(db_risk_matrix)
    db.commit()
    db.refresh(db_risk_matrix)

    business_process_2_data = db.query(Business_process_2).filter(
        Business_process_2.business_process_2_id == db_risk_matrix.business_process_2_id
    ).first()

    
    if business_process_2_data:
        response_data = RiskMatrixResponse(
            business_process_2_id = risk_matrix.business_process_2_id,
            business_process_2_name=business_process_2_data.business_process_2_name,
            business_process_1_name=business_process_2_data.business_process_1.business_process_1_name,
            owner=business_process_2_data.business_process_1.owner,
            step_business_process_2_level = risk_matrix.step_business_process_2_level,
            step_description = risk_matrix.step_description,
            step_performer = risk_matrix.step_performer,
            risk_code = risk_matrix.risk_code,
            risk_name = risk_matrix.risk_name,
            risk_description = risk_matrix.risk_description,
            control_procedure_code = risk_matrix.control_procedure_code,                       
            control_procedure_name = risk_matrix.control_procedure_name,
            control_procedure_owner = risk_matrix.control_procedure_owner,     
            control_procedure_description = risk_matrix.control_procedure_description,       
            control_procedure_inner_outer_document = risk_matrix.control_procedure_inner_outer_document,       
            control_procedure_frequency = risk_matrix.control_procedure_frequency,       
            control_procedure_type = risk_matrix.control_procedure_type,       
            control_procedure_category = risk_matrix.control_procedure_category,      
            effectivity_assessiskmatrixent = risk_matrix.effectivity_assessment,
            basis_of_assessment = risk_matrix.basis_of_assessment 
        )

    else:
        raise HTTPException(status_code=404, detail="BusinessProcess2 not found")

    return response_data 