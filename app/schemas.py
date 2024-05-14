from pydantic import BaseModel

class FoodBase(BaseModel):
    food_key: str
    food_name: str

class FoodBasic(FoodBase):
    food_representative : str | None
    manufacturing_company : str | None

    class Config:
        orm_mode: True

class FoodAll(FoodBasic):
    food_category : str
    kcal : int | None
    weight : float | None

    class Config:
        orm_mode: True

class ProcessedFoodBase(BaseModel):
    processed_food_key: str
    processed_food_name: str

class ProcessedFoodBasic(ProcessedFoodBase):
    processed_food_representative : str | None
    manufacturing_company : str | None
    
    class Config:
        orm_mode: True

class ProcessedFoodAll(ProcessedFoodBasic):
    processed_food_category : str
    kcal : int | None
    weight : float | None

    class Config:
        orm_mode: True