from sqlalchemy import Column, Integer, String, Numeric

from .database import Base

class Food(Base):
    __tablename__ = "food"

    food_key = Column(String, primary_key=True)
    food_name = Column(String, index=True)
    food_category = Column(String)
    food_representative = Column(String)
    kcal = Column(Integer)
    weight = Column(Numeric)
    manufacturing_company = Column(String)

class ProcessedFood(Base):
    __tablename__ = "processed_food"

    processed_food_key = Column(String, primary_key=True)
    processed_food_name = Column(String, index=True)
    processed_food_category = Column(String)
    processed_food_representative = Column(String)
    kcal = Column(Integer)
    weight = Column(Numeric)
    manufacturing_company = Column(String)