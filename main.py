import os
from fastapi import UploadFile
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import json
from loguru import logger
from fastapi.staticfiles import StaticFiles

logger.add("app.log", rotation="500 MB", retention="10 days", level="INFO")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:8000",
        "http://localhost:3000",
        'http://127.0.0.1:3000',
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CatCreate(BaseModel):
    name: str
    breed: str
    age: int


class Cat(CatCreate):
    id: int
    image: str = None


def configure_static(app):
    app.mount("/images", StaticFiles(directory="images"), name="images")


def read_cats_from_file():
    with open('cats.json') as f:
        cats_data = json.load(f)
        print(cats_data)
        return [Cat(**cat) for cat in cats_data]


def write_cats_to_file(cats):
    with open('cats.json', 'w') as f:
        cats_data = [cat.dict() for cat in cats]
        json.dump(cats_data, f)


def search_first_cat(**search_params) -> Cat:
    for cat in read_cats_from_file():
        for key in search_params.keys():
            if getattr(cat, key):
                if getattr(cat, key) == search_params[key]:
                    return cat
            else:
                raise Exception("Wrong parameter.")


@app.get('/cats', response_model=List[Cat])
async def get_cats():
    cats = read_cats_from_file()
    logger.info(f"Retrieved {len(cats)} cats from file.")
    return cats


@app.post('/cats', response_model=Cat)
async def create_cat(cat: CatCreate):
    cats = read_cats_from_file()
    new_cat_id = max(cat.id for cat in cats) + 1 if cats else 1
    new_cat = Cat(id=new_cat_id, **cat.dict())
    cats.append(new_cat)
    write_cats_to_file(cats)
    logger.info(f"Created new cat: {new_cat}")
    return new_cat


@app.post("/cats/{cat_id}/image", response_class=JSONResponse)
async def upload_cat_image(cat_id: int, image: UploadFile):
    cats = read_cats_from_file()
    cat_to_update = None
    for cat in cats:
        if cat.id == cat_id:
            cat_to_update = cat
            break
    if cat_to_update:
        with open(f"images/{cat_id}.jpg", "wb") as f:
            f.write(image.file.read())
        cat_to_update.image = "images/" + str(cat_id) + ".jpg"
        write_cats_to_file(cats)
        logger.info(f"Uploaded image for cat with id {cat_id}.")
        return {"message": "Image uploaded successfully."}
    else:
        logger.warning(f"Failed to upload image for cat with id {cat_id}. Cat not found.")
        return JSONResponse(status_code=404, content={"message": "Cat not found."})


@app.put('/cats/{cat_id}', response_model=Cat)
async def update_cat(cat_id: int, cat: CatCreate):
    cats = read_cats_from_file()
    cat_to_update = next((c for c in cats if c.id == cat_id), None)
    if cat_to_update:
        cat_to_update.name = cat.name
        cat_to_update.breed = cat.breed
        cat_to_update.age = cat.age
        write_cats_to_file(cats)
        logger.info(f"Updated cat with id {cat_id}: {cat_to_update}")
        return cat_to_update
    else:
        logger.warning(f"Failed to update cat with id {cat_id}. Cat not found.")
        return JSONResponse(status_code=404, content={"message": "Cat not found."})


@app.delete('/cats/{cat_id}', response_class=JSONResponse)
async def delete_cat(cat_id: int):
    cats = read_cats_from_file()
    cat = search_first_cat(id=cat_id)
    if cat.image:
        os.remove(cat.image)
    remaining_cats = [cat for cat in cats if cat.id != cat_id]
    write_cats_to_file(remaining_cats)
    logger.info(f"Deleted cat with id {cat_id}.")
    return {"message": "Cat deleted successfully."}


if __name__ == '__main__':
    import uvicorn

    configure_static(app)
    uvicorn.run(app, host='localhost', port=8000)
