import os
from fastapi import HTTPException, Depends, FastAPI, UploadFile

from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from PIL import Image
from io import BytesIO
from ultralytics import YOLO
import prrocr, re

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

#app = FastAPI()
path = "./best.pt"
model = YOLO(path)

@app.post("/food_detection")
async def predict_image(file: UploadFile = File(...)):
    image_data = BytesIO(await file.read())
    image = Image.open(image_data)
    results = model(image)

    response_data = []
    
    for r in results:
        cls_dict = r.names  
        for box, cls_number, conf in zip(r.boxes.xyxy, r.boxes.cls, r.boxes.conf):
            x1, y1, x2, y2 = map(int, box.tolist())
            cls_name = cls_dict[int(cls_number.item())]
            conf_number = float(conf.item())

            response_data.append({
                "bbox": [x1, y1, x2, y2],
                "cls_name": cls_name,
                "confidence": round(conf_number, 2)
            })

    return JSONResponse(content=response_data)

@app.post("/ocr/")
async def ocr(file: UploadFile, db: Session = Depends(get_db)):
    try:
        contents = await file.read()
        UPLOAD_DIR = "app/receipt"
        filename = f"receipt.jpg"
        with open(os.path.join(UPLOAD_DIR, filename), "wb") as fp:
            fp.write(contents)
        
        ocr = prrocr.ocr(lang="ko")

        ocr_result = ocr(filename)
        ocr_text = ' '.join

        pattern = re.compile(r'([가-힣\w\s\(\);]+) \d{1,3}(,\d{3})*')

        matches = pattern.findall(ocr_text)

        name_list = [re.sub(r'^[^가-힣\w]+|[^가-힣\w]+$', '', match[0]).strip() for match in matches]
        
        result = []

        # 음식 정보 순환 조회
        for food_name in name_list:
            foods = crud.get_food(db=db, food_name=food_name)
            result.extend(foods)

        # 가공식품 정보 조회
        for processed_food_name in name_list:
            processed_foods = crud.get_processed_food(db=db, processed_food_name=processed_food_name)
            result.extend(processed_foods)

        # 원재료성 식품 정보 조회
        for raw_food_name in name_list:
            raw_foods = crud.get_processed_food(db=db, raw_name=raw_food_name)
            result.extend(raw_foods)

        return result
    
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))




