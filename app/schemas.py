from pydantic import BaseModel

class FoodBase(BaseModel):
    food_key: str
    food_name: str
    food_representative : str | None

class SubFood(FoodBase):
    food_category : str
    manufacturing_company : str | None
    kcal : int | None
    weight : float | None

    class Config:
        orm_mode: True

class ProcessedFoodBase(BaseModel):
    processed_food_key: str
    processed_food_name: str
    processed_food_representative : str | None

class SubProcessedFood(ProcessedFoodBase):
    processed_food_category: str
    manufacturing_company : str | None
    kcal : int | None
    weight : float | None

    class Config:
        orm_mode: True

class RawFoodBase(BaseModel):
    raw_food_key: str
    raw_food_name: str
    raw_food_category: str