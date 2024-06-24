from sqlalchemy.orm import Session, load_only

from . import models, schemas


def get_food(db: Session, food_name: str):
    return db.query(models.Food).filter(models.Food.food_name.like(f"%{food_name}%")).all()

def get_processed_food(db: Session, processed_food_name: str):
    return db.query(models.ProcessedFood).filter(models.ProcessedFood.processed_food_name.like(f"%{processed_food_name}%")).all()

def get_raw_food(db: Session, raw_food_name: str):
    return db.query(models.RawFood).filter(models.RawFood.raw_food_name.like(f"%{raw_food_name}%")).all()

def get_all_food_name(db: Session):
    all_foods = db.query(models.Food.food_name).all()
    all_processed_foods = db.query(models.ProcessedFood.processed_food_name).all()
    all_raw_foods = db.query(models.RawFood.raw_food_name).all()

    all_food_names = [food.food_name for food in all_foods]
    all_processed_food_names = [processed_food.processed_food_name for processed_food in all_processed_foods]
    all_raw_food_names = [raw_food.raw_food_name for raw_food in all_raw_foods]

    combined_food_names = all_food_names + all_processed_food_names + all_raw_food_names
    
    return combined_food_names

def get_all_food(db: Session, food_name: str):
    result = db.query(models.RawFood).filter(models.RawFood.raw_food_name.like(f"{food_name}")).all()
    if result:
        return result
    result = db.query(models.Food).filter(models.Food.food_name.like(f"{food_name}")).all()
    if result:
        return result
    result = db.query(models.ProcessedFood).filter(models.ProcessedFood.processed_food_name.like(f"{food_name}")).all()
    if result:
        return result
    