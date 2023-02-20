from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import json
from loguru import logger

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
    'http://192.168.1.150:3000',  # self ip with react
    'http://127.0.0.1:3000',
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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


def read_cats_from_file():
    with open('cats.json') as f:
        cats_data = json.load(f)
        return [Cat(**cat) for cat in cats_data]


def write_cats_to_file(cats):
    with open('cats.json', 'w') as f:
        cats_data = [cat.dict() for cat in cats]
        json.dump(cats_data, f)


@app.get('/cats', response_model=List[Cat])
async def get_cats():
    cats = read_cats_from_file()
    logger.info(f"Retrieved {len(cats)} cats from file.")
    return cats


@app.post('/cats', response_model=Cat)
async def create_cat(cat: CatCreate):
    cats = read_cats_from_file()
    new_cat_id = max(cat.id for cat in cats) + 1
    new_cat = Cat(id=new_cat_id, **cat.dict())
    cats.append(new_cat)
    write_cats_to_file(cats)
    logger.info(f"Created new cat: {new_cat}")
    return new_cat


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
    remaining_cats = [cat for cat in cats if cat.id != cat_id]
    write_cats_to_file(remaining_cats)
    logger.info(f"Deleted cat with id {cat_id}.")
    return {"message": "Cat deleted successfully."}


if __name__ == '__main__':
    import uvicorn
    logger.add("file_{time}.log")
    uvicorn.run(app, host='localhost', port=8000)