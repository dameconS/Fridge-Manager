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
from typing import Union

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

@app.get("/findfood/{food_name}", response_model=list[schemas.FoodBase])
def read_foods(food_name: str, db: Session = Depends(get_db)):
    foods = crud.get_food(db=db, food_name=food_name)
    return foods

@app.get("/findprocessedfood/{processed_food_name}", response_model=list[schemas.ProcessedFoodBase])
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


@app.post("/ocr/", response_model=list[Union[schemas.FoodBase, schemas.ProcessedFoodBase, schemas.RawFoodBase]])
async def ocr(file: UploadFile, db: Session = Depends(get_db)):
    contents = await file.read()
    UPLOAD_DIR = "app/receipt"
    filename = f"receipt.jpg"
    with open(os.path.join(UPLOAD_DIR, filename), "wb") as fp:
        fp.write(contents)

    ocr = prrocr.ocr(lang="ko")

    ocr_result = ocr(contents)

    ocr_text = ' '.join(ocr_result)

    items = re.findall(r'\b[가-힣]+\s?[가-힣]*[0-9]*[g|L]*\b', ocr_text)

    foods = crud.get_all_food_name(db=db)

    import difflib

    def find_most_similar(search_list, sample_list):
        most_similar_words = []
        for word in search_list:
            most_similar = difflib.get_close_matches(word, sample_list, n=1, cutoff=0.6)
            if most_similar:
                most_similar_words.append(most_similar[0])
        return most_similar_words
    
    food_list = find_most_similar(items ,foods)

    response = []

    for food_name in food_list:
        result = crud.get_all_food(db=db, food_name=food_name)
        response.append(result[0])

    return response