from sqlalchemy.orm import Session, load_only

from . import models, schemas


def get_food(db: Session, food_name: str):
    return db.query(models.Food).filter(models.Food.food_name.like(f"%{food_name}%")).all()

def get_processed_food(db: Session, processed_food_name: str):
    return db.query(models.ProcessedFood).filter(models.ProcessedFood.processed_food_name.like(f"%{processed_food_name}%")).all()