import os
from fastapi import HTTPException, Depends, FastAPI, UploadFile

from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(exc))
    finally:
        db.close()

@app.get("/findfood/{food_name}", response_model=list[schemas.FoodBasic])
def read_foods(food_name: str, db: Session = Depends(get_db)):
    foods = crud.get_food(db=db, food_name=food_name)
    return foods

@app.get("/findprocessedfood/{processed_food_name}", response_model=list[schemas.ProcessedFoodBasic])
def read_processed_foods(processed_food_name: str, db: Session = Depends(get_db)):
    processed_foods = crud.get_processed_food(db=db, processed_food_name=processed_food_name)
    return processed_foods

# @app.post("/ocr/")
# async def ocr(file: UploadFile, db: Session = Depends(get_db)):
#     try:
#         contents = await file.read()
#         UPLOAD_DIR = "app/receipt"
#         filename = f"receipt.jpg"
#         with open(os.path.join(UPLOAD_DIR, filename), "wb") as fp:
#             fp.write(contents)
#         name_list = scanner.ocr()
#         result = name_list

#         # 음식 이름 리스트를 순회하면서 데이터베이스 조회
#         for food_name in name_list:
#             foods = crud.get_food(db=db, food_name=food_name)
#             result.extend(foods)

#         # 처리된 음식 정보도 조회
#         for processed_food_name in name_list:
#             processed_foods = crud.get_processed_food(db=db, processed_food_name=processed_food_name)
#             result.extend(processed_foods)

#         return result
    
#     except Exception as exc:
#         raise HTTPException(status_code=500, detail=str(exc))