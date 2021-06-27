from typing import List

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from . import crud, schemas
from .database import SessionLocal

app = FastAPI()


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
def read_parties(skip: int = 0,
                 limit: int = 100,
                 db: Session = Depends(get_db)):
    parties = crud.get_parties(db, skip=skip, limit=limit)
    return parties


@app.get("/politicians", response_model=List[schemas.Politician])
def read_politicians(party: int = 0,
                     skip: int = 0,
                     limit: int = 100,
                     db: Session = Depends(get_db)):
    politicians = crud.get_politicians(party, db, skip=skip, limit=limit)
    return politicians


@app.get("/politicians/{politicId}", response_model=schemas.Politician)
def read_politician(politicianId: str, db: Session = Depends(get_db)):
    return crud.get_politician(politicianId, db)


@app.get("/words", response_model=List[schemas.Word])
def read_words(politic: int = 0,
               skip: int = 0,
               limit: int = 100,
               db: Session = Depends(get_db)):
    return crud.get_words(politic, db, skip=skip, limit=limit)


@app.get("/words/sejm", response_model=List[schemas.Word])
def read_words_for_sejm(skip: int = 0,
                        limit: int = 100,
                        db: Session = Depends(get_db)):
    return crud.get_words_for_sejm(0, db, skip=skip, limit=limit)


@app.get("/words/party", response_model=List[schemas.Word])
def read_words_for_party(skip: int = 0,
                         limit: int = 100,
                         db: Session = Depends(get_db)):
    return crud.get_words_for_party(0, db, skip=skip, limit=limit)
