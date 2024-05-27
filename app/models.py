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

class RawFood(Base):
    __tablename__ = "raw_food"

    raw_food_key = Column(String, primary_key=True)
    raw_food_name = Column(String, index=True)
    raw_food_category = Column(String)
    kcal = Column(Integer)
    moisture_g = Column(Numeric)
    protein_g = Column(Numeric)
    fat_g = Column(Numeric)
    ash_g = Column(Numeric)
    carbohydrate_g = Column(Numeric)
    sugars_g = Column(Numeric)
    dietary_fiber_g = Column(Numeric)
    calcium_mg = Column(Numeric)
    iron_mg = Column(Numeric)
    phosphorus_mg = Column(Numeric)
    potassium_mg = Column(Numeric)
    sodium_mg = Column(Numeric)
    vitamin_a_ug_rae = Column(Numeric)
    vitamin_c_mg = Column(Numeric)
    vitamin_d_ug = Column(Numeric)
    cholesterol_mg = Column(Numeric)
    saturated_fat_g = Column(Numeric)
    trans_fat_g = Column(Numeric)