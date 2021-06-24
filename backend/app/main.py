from typing import List
import json

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session, query

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    with open("./app/data/parties.json", 'r') as politicians_json:
        parties = json.load(politicians_json)
    with SessionLocal() as db:
        crud.delete_all_parties(db)
        crud.delete_all_politicians(db)
        for party in parties:
            new_party = models.Party(
                id=party["party_ID"],
                name=party['Party']
            )
            for politician in party["Politicians"]:
                new_politician = models.Politician(
                    twitter_id=politician['ID'],
                    name=politician['Name'],
                    party_id=party["party_ID"]
                )
                db.add(new_politician)
            db.add(new_party)
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


@app.get("/parties", response_model=List[schemas.Party])
def read_parties(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    parties = crud.get_parties(db, skip=skip, limit=limit)
    return parties


@app.get("/politicians", response_model=List[schemas.Politician])
def read_politicians(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    politicians = crud.get_politicians(db, skip=skip, limit=limit)
    return politicians
