from sqlalchemy.orm import Session, query, session

from . import models, schemas

#Items crud

def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_item(db: Session, item: schemas.ItemCreate):
    new_item = models.Item(**item.dict())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


def delete_all_items(db: Session):
    try:
        db.query(models.Item).delete()
        db.commit()
    except:  # noqa
        db.rollback()

# Party crud

def get_parties(db:Session, skip: int = 0, limit: int =100):
    return db.query(models.Party).offset(skip).limit(limit).all()

def create_party(db: Session, party: schemas.PartyCreate):
    new_party = models.Party(**party.dict())
    db.add(new_party)
    db.commit()
    db.refresh(new_party)
    return new_party

def delete_all_parties(db: Session):
    try:
        db.query(models.Party).delete()
        db.commit()
    except: 
        db.rollback()


# Polticians crud 

def get_politicians(db: Session, skip: int = 0, limit: int =100):
    return db.query(models.Politician).offset(skip).limit(limit).all()

def create_politician(db: Session, politician: schemas.PoliticianCreate):
    new_politician = models.Politician(**politician.dict())
    db.add(new_politician)
    db.commit()
    db.refresh(new_politician)
    return new_politician

def delete_all_politicians(db: Session):
    try:
        db.query(models.Politician).delete()
        db.commit()
    except:
        db.rollback()

#Word crud 

def get_words(db: Session, skip: int = 0, limit: int =100):
    return db.query(models.Word).offset(skip).limit(limit).all()

# WordIndex crud

def get_word_index(db: Session, skip: int = 0, limit: int =100):
    return db.query(models.WordIndex).offset(skip).limit(limit).all()