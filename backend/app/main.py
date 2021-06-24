from typing import List
import json

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    things = None
    with open('./app/data/things.json', 'r') as json_file:
        things = json.load(json_file)
    with SessionLocal() as db:
        crud.delete_all_items(db)
        for thing in things:
            new_thing = models.Item(
                title=thing['title'],
                description="empty"
            )
            db.add(new_thing)
        db.commit()

# dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items
