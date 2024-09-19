from typing import Optional
from fastapi import HTTPException, Path, Query 
from fastapi import APIRouter, Depends
from fastapi import Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from pydantic import ValidationError

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, update, func, Integer, cast, String
from sqlalchemy.sql import text
from sqlalchemy.orm import Session, DeclarativeMeta

from config.database import conn, get_db
from schemas.reestr_schemas import RiskFactor1Create, RiskFactor2Create, RiskFactor3Create, RiskFactor4Create, RiskFactor2EventCreate, RiskFactor2EventBase
from models.reestr import RiskFactor1, RiskFactor2, RiskFactor3, RiskFactor4, RiskCategory, RiskFactor2Event, Divisions

from modules.recursive_calc import update_risk_factor_3_from_4, update_risk_factor_2_from_3, update_risk_factor_1_from_2
from modules.calculations import calculate_residual_loss

from .users_router import get_current_user  

reestr_routers = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@reestr_routers.post("/reestr/risk_factor_1/", response_model=int, tags=['reestr'])
def create_risk_factor_1(risk_factor_1: RiskFactor1Create, db: Session = Depends(get_db)):


    risk_category = db.query(RiskCategory).filter_by(risk_code=risk_factor_1.risk_code).first()

    if not risk_category:
        raise HTTPException(status_code=404, detail="Risk Category not found")


    next_number = (
        db.query(func.max(cast(
            func.substr(RiskFactor1.level_1_id, func.length(risk_category.risk_code) + 2),
            Integer
        )))
        .filter(RiskFactor1.risk_code == risk_category.risk_code)
        .filter(cast(func.substr(RiskFactor1.level_1_id, func.length(risk_category.risk_code) + 2), Integer) is not None)
        .scalar() or 0
    ) + 1

    next_level_1_id = f"{risk_category.risk_code}-{next_number}"


    db_risk_factor_1 = RiskFactor1(**risk_factor_1.dict(), level_1_id = next_level_1_id)
    db.add(db_risk_factor_1)
    db.commit()
    db.refresh(db_risk_factor_1)

    return db_risk_factor_1.level_1_id


@reestr_routers.post("/reestr/risk_factor_2/", response_model=int, tags=['reestr'])
def create_risk_factor_2(risk_factor_2: RiskFactor2Create, db: Session = Depends(get_db), 
                    level_1_id: Optional[str] = Query(None, title="Level 1 ID", description="ID of the parent RiskFactor1")):

    print("Received level_1_id:", risk_factor_2.level_1_id)
   
    last_id = (
        db.query(RiskFactor2.level_2_id)
        .filter(RiskFactor2.level_2_id.like(f"{risk_factor_2.level_1_id}.%"))
        .order_by(func.cast(func.split_part(RiskFactor2.level_2_id, '.', 2), Integer).desc())
        .first()
    )

    if last_id:
        next_number = int(last_id[0].split('.')[-1]) + 1
        next_level_2_id = f"{risk_factor_2.level_1_id}.{next_number}"
    else:
        next_level_2_id = f"{risk_factor_2.level_1_id}.1"

    loss_2 = risk_factor_2.prob * risk_factor_2.effect

    db_risk_factor_2 = RiskFactor2(**risk_factor_2.dict(), loss=loss_2, level_2_id = next_level_2_id)
    db.add(db_risk_factor_2)
    db.commit()
    db.refresh(db_risk_factor_2)

    update_risk_factor_1_from_2(db, risk_factor_2.level_1_id)

    return db_risk_factor_2.level_2_id


@reestr_routers.post("/reestr/risk_factor_3/", response_model=int, tags=['reestr'])
def create_risk_factor_3(risk_factor_3: RiskFactor3Create, db: Session = Depends(get_db), 
                         level_2_id: Optional[str] = Query(None, title = 'Level 2 ID', description = 'ID of the parent RiskFactor2')):

    last_id = (
        db.query(RiskFactor3.level_3_id)
        .filter(RiskFactor3.level_3_id.like(f"{risk_factor_3.level_2_id}.%"))
        .order_by(func.cast(func.split_part(RiskFactor3.level_3_id, '.', 3), Integer).desc())
        .first()
    )

    if last_id:
        # Extract the last number and increment
        next_number = int(last_id[0].split('.')[-1]) + 1
        next_level_3_id = f"{risk_factor_3.level_2_id}.{next_number}"
    else:
        # If no previous IDs, start with 1
        next_level_3_id = f"{risk_factor_3.level_2_id}.1"


    
    loss_3 = risk_factor_3.prob * risk_factor_3.effect


    # Создание объекта RiskFactor3 с вычисленными значениями
    db_risk_factor_3 = RiskFactor3(**risk_factor_3.dict(), loss=loss_3, level_3_id=next_level_3_id)


    db.add(db_risk_factor_3)
    db.commit()
    db.refresh(db_risk_factor_3)    

    update_risk_factor_2_from_3(db, risk_factor_3.level_2_id)
    update_risk_factor_1_from_2(db, risk_factor_3.level_2_id)

    return db_risk_factor_3.level_3_id


@reestr_routers.post("/reestr/risk_factor_4/", response_model=int, tags=['reestr'])
def create_risk_factor_4(risk_factor_4: RiskFactor4Create, db: Session = Depends(get_db), 
                         level_3_id: Optional[str] = Query(None, title = 'Level 3 ID', description = 'ID of the parent RiskFactor3')):


    last_id = (db.query(RiskFactor4.level_4_id).filter(RiskFactor4.level_4_id.like(f"{risk_factor_4.level_3_id}.%")).order_by(func.cast(
        func.split_part(RiskFactor4.level_4_id, '.', 4), Integer).desc()).first())

    if last_id:
        next_number = int(last_id[0].split('.')[-1]) + 1
        next_level_4_id = f"{risk_factor_4.level_3_id}.{next_number}"
    else:
        next_level_4_id = f"{risk_factor_4.level_3_id}.1"

    loss_4 = risk_factor_4.prob * risk_factor_4.effect

    
    
    level_4_factors = db.query(RiskFactor4).filter(RiskFactor4.level_4_id.like(f"{level_3_id}.%")).all()
    if level_4_factors:
        for factor_4 in level_4_factors:
            # Вычисляем residual_loss для каждого фактора уровня 4
            effect = "нет данных" 
            risk_factor_3 = db.query(RiskFactor3).filter_by(level_3_id=level_3_id).first()
            if risk_factor_3:
                risk_factor_2 = db.query(RiskFactor2).filter_by(level_2_id=risk_factor_3.level_2_id).first()
                if risk_factor_2:
                    risk_factor_2_event = db.query(RiskFactor2Event).filter_by(level_2_id=risk_factor_2.level_2_id).first()
                    if risk_factor_2_event:
                        effect = risk_factor_2_event.event_effectiveness

            residual_loss_4 = calculate_residual_loss(factor_4.loss, effect)

    db_risk_factor_4 = RiskFactor4(**risk_factor_4.dict(), loss=loss_4, residual_loss=residual_loss_4, level_4_id = next_level_4_id)
    db.add(db_risk_factor_4)
    db.commit()
    db.refresh(db_risk_factor_4)

    update_risk_factor_3_from_4(db, risk_factor_4.level_3_id)

    return db_risk_factor_4.level_4_id

@reestr_routers.post("/reestr/risk_factor_2/{level_2_id}/events", response_model=RiskFactor2EventBase, tags=['reestr'])
def create_risk_factor_2_event(level_2_id: str, event_data: RiskFactor2EventCreate, db: Session = Depends(get_db)):
    db_event = RiskFactor2Event(
        event_name=event_data.event_name,
        responsible_sp=event_data.responsible_sp,
        event_effectiveness=event_data.event_effectiveness,
        level_2_id=level_2_id
    )    
    
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


@reestr_routers.get('/reestr/structure_divisions_table', response_model=list, tags=["reestr"])
async def fetch_subsidiary_reestr(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    # Apply filtering based on user's position
    query = (
        select(
            RiskCategory.risk_category_name,
            RiskFactor1.level_1_id,
            RiskFactor1.owner,
            RiskFactor1.risk_code,
            RiskFactor1.control_sp,
            RiskFactor1.description_1,
            RiskFactor2.description_2,
            RiskFactor3.description_3,
            RiskFactor4.description_4,
            RiskFactor2.swot,
            RiskFactor2Event.event_name,
            RiskFactor2Event.event_effectiveness,
            RiskFactor2Event.responsible_sp,
            RiskFactor1.total_prob.label('prob_1'),
            RiskFactor1.total_effect.label('effect_1'),
            RiskFactor1.total_loss.label('loss_1')
        )
        .join(RiskFactor1, RiskCategory.risk_code == RiskFactor1.risk_code)
        .outerjoin(RiskFactor2, RiskFactor1.level_1_id == RiskFactor2.level_1_id)
        .outerjoin(RiskFactor3, RiskFactor2.level_2_id == RiskFactor3.level_2_id)
        .outerjoin(RiskFactor4, RiskFactor3.level_3_id == RiskFactor4.level_3_id)
        .outerjoin(RiskFactor2Event, RiskFactor2Event.level_2_id == RiskFactor2.level_2_id)
        .where(RiskFactor1.division_id == current_user.workplace)  # Фильтр по месту работы
  
    )
    result = db.execute(query).fetchall()
    return result


@reestr_routers.get('/reestr/main_table', response_model=list, tags=["reestr"])
async def fetch_all_reestr(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    # Retrieve the workplace name based on the workplace_id from the current_user
    workplace_id = current_user.workplace
    workplace_name = db.query(Divisions.division_name).filter(Divisions.division_id == workplace_id).scalar()
    print('mesto raboty:', workplace_name) 

    # Check if the user has permission to access the data
    if workplace_name != 'Центральный аппарат':
        return []
    # Define the query
    query = (
        select(
            RiskCategory.risk_category_name,
            RiskFactor1.level_1_id,
            RiskFactor1.owner,
            RiskFactor1.risk_code,
            RiskFactor1.control_sp,
            RiskFactor1.description_1,
            RiskFactor2.description_2,
            RiskFactor3.description_3,
            RiskFactor4.description_4,
            RiskFactor2.swot,
            RiskFactor2Event.event_name,
            RiskFactor2Event.event_effectiveness,
            RiskFactor2Event.responsible_sp,
            RiskFactor1.total_prob.label('prob_1'),
            RiskFactor1.total_effect.label('effect_1'),
            RiskFactor1.total_loss.label('loss_1')
        )
        .join(RiskFactor1, RiskCategory.risk_code == RiskFactor1.risk_code)
        .outerjoin(RiskFactor2, RiskFactor1.level_1_id == RiskFactor2.level_1_id)
        .outerjoin(RiskFactor3, RiskFactor2.level_2_id == RiskFactor3.level_2_id)
        .outerjoin(RiskFactor4, RiskFactor3.level_3_id == RiskFactor4.level_3_id)
        .outerjoin(RiskFactor2Event, RiskFactor2Event.level_2_id == RiskFactor2.level_2_id)
    )
    
    # Execute the query
    result = db.execute(query).fetchall()

    return result


@reestr_routers.get('/reestr/risk_category_name/', response_model=list, tags=['reestr'])
async def fetch_risk_categories(db: Session = Depends(get_db)):
    query = (
        select(
            RiskCategory.risk_category_name,
            RiskCategory.risk_code
        )
    )   
    result = db.execute(query).fetchall()
    return [{"risk_category_name": row[0], "risk_code": row[1]} for row in result]


@reestr_routers.get('/reestr/description_1/{risk_category_name}', response_model=list, tags=['reestr'])
async def fetch_risk_1_description_by_category(risk_category_name: str, db: Session = Depends(get_db)):
    risk_category = db.query(RiskCategory).filter(RiskCategory.risk_category_name == risk_category_name).first()
    if not risk_category:
        raise HTTPException(status_code=404, detail="Категория риска не найдена")
    
    query = (
        db.query(RiskFactor1)
        .join(RiskCategory, RiskFactor1.risk_code == RiskCategory.risk_code)
        .filter(RiskCategory.risk_category_name == risk_category_name)
        .all()
    )
    
    descriptions = [{"level_1_id": item.level_1_id, "description_1": item.description_1} for item in query]
    
    return descriptions


@reestr_routers.get("/reestr/description_2/{level_1_id}", response_model=list, tags=['reestr'])
async def fetch_risk_2_description_by_level_1_id(level_1_id: str, db: Session = Depends(get_db)):

    risk_factor_2_descriptions = (
        db.query(RiskFactor2)
        .join(RiskFactor1, RiskFactor2.level_1_id == RiskFactor1.level_1_id)
        .filter(RiskFactor1.level_1_id == level_1_id)
        .all()
    )
    descriptions = [{"level_2_id": item.level_2_id, "description_2": item.description_2} for item in risk_factor_2_descriptions]
    
    return descriptions



@reestr_routers.get("/reestr/description_3/{level_2_id}", response_model=list, tags=['reestr'])
async def fetch_risk_3_description_by_level_2_id(level_2_id: str, db: Session = Depends(get_db)):
    risk_factor_3_descriptions = (
        db.query(RiskFactor3)
        .join(RiskFactor2, RiskFactor3.level_2_id == RiskFactor2.level_2_id)
        .filter(RiskFactor2.level_2_id == level_2_id)
        .all()
    )
    
    descriptions = [{"level_3_id": item.level_3_id, "description_3": item.description_3} for item in risk_factor_3_descriptions]
    
    return descriptions

@reestr_routers.get("/reestr/description_4/{level_3_id}", response_model=list, tags=['reestr'])
async def fetch_risk_4_description_by_level_3_id(level_3_id: str, db: Session = Depends(get_db)):
    risk_factor_4_descriptions = (
        db.query(RiskFactor4)
        .join(RiskFactor3, RiskFactor4.level_3_id == RiskFactor3.level_3_id)
        .filter(RiskFactor3.level_3_id == level_3_id)
        .all()
    )
    
    descriptions = [{"level_4_id": item.level_4_id, "description_4": item.description_4} for item in risk_factor_4_descriptions]
    
    return descriptions


# Need to complete / corrections
@reestr_routers.delete('/reestr/{level}/{item_id}', tags=["reestr"])
async def delete_reestr(level: str, item_id:str = None, db: Session = Depends(get_db)):

    # if level == 'RiskCategory':
    #     item = db.query(RiskCategory).filter(RiskCategory.risk_code == item_id).first()

    if level == 'risk_factor_1':
        item = db.query(RiskFactor1).filter(RiskFactor1.level_1_id == item_id).first()

    if level == 'risk_factor_2':
        item = db.query(RiskFactor2).filter(RiskFactor2.level_2_id == item_id).first()

    if level == 'RiskFactor3':
        item = db.query(RiskFactor3).filter(RiskFactor3.level_3_id == item_id).first()

    if level == 'RiskFactor4':
        item = db.query(RiskFactor4).filter(RiskFactor4.level_4_id == item_id).first()

    
    if item:
        db.delete(item)
        db.commit()
        return {"message": "Item deleted successfully"}
    else:
        # Step 6: Return a 404 response if the item doesn't exist
        raise HTTPException(status_code=404, detail="Item not found")

    # return conn.execute(select(RiskFactor1).where(Users.id == id)).first()

