from sqlalchemy.orm import Session
from sqlalchemy import select, update, func, Integer, cast, String

from models.reestr import RiskFactor1, RiskFactor2, RiskFactor3, RiskFactor4, RiskCategory, RiskFactor2Event
from modules.calculations import calculate_residual_loss, calculate_condition





def update_risk_factor_3_from_4(db: Session, level_3_id: str):

    db_risk_factor_3 = db.query(RiskFactor3).filter_by(level_3_id=level_3_id).first()

    if db_risk_factor_3:
        # Получаем сумму значений всех факторов уровня 4 под этим уровнем 3
        avg_values = db.query(
            func.avg(RiskFactor4.prob).label("prob_avg"),
            func.avg(RiskFactor4.effect).label("effect_avg"),
        ).filter(RiskFactor4.level_4_id.like(f"{level_3_id}.%")).first()

        if avg_values:
            # Обновляем фактор уровня 3 суммарными значениями
            db_risk_factor_3.prob = avg_values.prob_avg or 0.0
            db_risk_factor_3.effect = avg_values.effect_avg or 0.0
            db_risk_factor_3.loss = db_risk_factor_3.prob * db_risk_factor_3.effect

# Получаем значение эффекта из таблицы RiskFactor2Event
            risk_factor_2 = db.query(RiskFactor2).filter_by(level_2_id=db_risk_factor_3.level_2_id).first()
            if risk_factor_2:
                risk_factor_2_event = db.query(RiskFactor2Event).filter_by(level_2_id=risk_factor_2.level_2_id).first()
                if risk_factor_2_event:
                    effect = risk_factor_2_event.event_effectiveness
                else:
                    effect = "нет данных"
            else:
                effect = "нет данных"

            # Вычисляем Residual Loss с учетом полученного эффекта
            residual_loss = calculate_residual_loss(db_risk_factor_3.loss, effect)
            db_risk_factor_3.residual_loss = residual_loss

            db.commit()

            # Обновляем фактор уровня 2 и уровня 1
            level_2_id = level_3_id.rsplit('.', 1)[0]
            update_risk_factor_2_from_3(db, level_2_id)
            level_1_id = level_2_id.split('.', 1)[0]
            update_risk_factor_1_from_2(db, level_1_id)
        else:
            print(f"No level 4 factors found for level 3 ID: {level_3_id}")
    else:
        print(f"Corresponding level 3 factor not found for level 3 ID: {level_3_id}")

# Function to update RiskFactor2 from RiskFactor3
def update_risk_factor_2_from_3(db: Session, level_2_id: str):
    # Get the corresponding level 2 factor
    db_risk_factor_2 = db.query(RiskFactor2).filter_by(level_2_id=level_2_id).first()

    if db_risk_factor_2:
        # Get the avg of values from all level 3 factors under this level 2
        avg_values = db.query(
            func.avg(RiskFactor3.prob).label("prob_avg"),
            func.avg(RiskFactor3.effect).label("effect_avg"),
            # func.avg(RiskFactor3.loss).label("loss_avg")
        ).filter(RiskFactor3.level_3_id.like(f"{level_2_id}.%")).first()

        if avg_values:
            # Update level 2 factor with the avg values
            db_risk_factor_2.prob = avg_values.prob_avg or 0.0
            db_risk_factor_2.effect = avg_values.effect_avg or 0.0
            db_risk_factor_2.loss =  db_risk_factor_2.prob * db_risk_factor_2.effect

# Получаем значение эффекта из таблицы RiskFactor2Event
            risk_factor_2 = db.query(RiskFactor2).filter_by(level_2_id=db_risk_factor_2.level_2_id).first()
            if risk_factor_2:
                risk_factor_2_event = db.query(RiskFactor2Event).filter_by(level_2_id=risk_factor_2.level_2_id).first()
                if risk_factor_2_event:
                    effect = risk_factor_2_event.event_effectiveness
                else:
                    effect = "нет данных"
            else:
                effect = "нет данных"

            # Вычисляем Residual Loss с учетом полученного эффекта
            residual_loss_2 = calculate_residual_loss(db_risk_factor_2.loss, effect)
            db_risk_factor_2.residual_loss = residual_loss_2

            # Commit the changes
            db.commit()

            level_1_id = level_2_id.rsplit('.', 1)[0]
            update_risk_factor_1_from_2(db, level_1_id)
        else:
            print(f"No level 3 factors found for level 2 ID: {level_2_id}")
    else:
        print(f"Corresponding level 2 factor not found for level 2 ID: {level_2_id}")


# Function to update RiskFactor1 from RiskFactor2
def update_risk_factor_1_from_2(db: Session, level_1_id: str):
    # Get the avg of values from all level 2 factors
    db_risk_factor_1 = db.query(RiskFactor1).filter_by(level_1_id=level_1_id).first()

    if db_risk_factor_1:
        avg_values = db.query(
            func.sum(RiskFactor2.effect).label("effect_sum"),
        ).filter(RiskFactor2.level_2_id.like(f"{level_1_id}.%")).first()

        if avg_values:
            total_prob = calculate_condition(
                [factor.loss for factor in db.query(RiskFactor2).filter_by(level_1_id=level_1_id)],
                [factor.prob for factor in db.query(RiskFactor2).filter_by(level_1_id=level_1_id)]
            )
            
            total_effect = avg_values.effect_sum or 0.0
            total_loss = total_prob * total_effect

            db_risk_factor_1.total_prob = total_prob
            db_risk_factor_1.total_effect = total_effect
            db_risk_factor_1.total_loss = total_loss

# Получаем значение эффекта из таблицы RiskFactor2Event
            risk_factor_2 = db.query(RiskFactor2).filter_by(level_1_id=db_risk_factor_1.level_1_id).first()
            if risk_factor_2:
                risk_factor_2_event = db.query(RiskFactor2Event).filter_by(level_2_id=risk_factor_2.level_2_id).first()
                if risk_factor_2_event:
                    effect = risk_factor_2_event.event_effectiveness
                else:
                    effect = "нет данных"
            else:
                effect = "нет данных"


            residual_loss_1 = calculate_residual_loss(total_loss, effect)

            db_risk_factor_1.residual_loss = residual_loss_1

                # Commit the changes
            db.commit()
        else:
            # Handle the case where no level 2 factors are found
            print("No level 2 factors found for updating level 1")