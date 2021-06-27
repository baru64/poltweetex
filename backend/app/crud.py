from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from . import models, schemas
from sqlalchemy.sql.expression import func

# Party crud


def get_parties(db: Session, skip: int = 0, limit: int = 100):
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
    except Exception:
        db.rollback()


# Polticians crud

def get_politicians(party: int, db: Session, skip: int = 0, limit: int = 100):
    if(party == 0):
        return db.query(models.Politician).offset(skip).limit(limit).all()
    else:
        return db.query(models.Politician).filter(
            models.Politician.party_id == party
        ).offset(skip).limit(limit).all()


def get_politician(politicianId: str, db: Session):
    return db.query(models.Politician).filter(
        models.Politician.twitter_id == politicianId
    ).one()


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
    except Exception:
        db.rollback()

# Word crud


def get_words(politic, db: Session, minusDays: datetime = 7, skip: int = 0, limit: int = 100):
    date = datetime.now() - timedelta(minusDays)
    words = db.query(models.Word).filter(
        models.Word.politician_id == str(politic)
    ).filter(
        func.length(models.Word.word) > 1
    ).filter(
        models.Word.date > date).order_by(
            models.Word.count.desc()).offset(skip).limit(limit).all()
    return mergeWords(words)


def get_words_for_sejm(db: Session, minusDays: int = 7, skip: int = 0, limit: int = 100):
    date = datetime.now() - timedelta(minusDays)
    words = db.query(models.Word).filter(
        func.length(models.Word.word) > 1).filter(
            models.Word.date > date).order_by(
        models.Word.count.desc()).offset(skip).limit(limit).all()
    return mergeWords(words)


def get_words_for_party(party: int, db: Session, minusDays: datetime = 7, skip: int = 0, limit: int = 100):
    date = datetime.now() - timedelta(minusDays)
    politciansIds = []
    politiciansObject = db.query(models.Politician).filter(
        models.Politician.party_id == party).all()
    for obj in politiciansObject:
        politciansIds.append(obj.twitter_id)
    words = db.query(models.Word).filter(
        models.Word.politician_id in politciansIds
    ).filter(models.Word.date > date).filter(
        func.length(models.Word.word) > 1
    ).order_by(models.Word.count.desc()).offset(skip).limit(limit).all()
    return mergeWords(words)


# WordIndex crud


def get_word_index(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.WordIndex).filter(
        func.length(models.Word.word) > 1
    ).offset(skip).limit(limit).all()


def mergeWords(words):
    for i, word in enumerate(words):
        for j, wordv2 in enumerate(words):
            if word.word == wordv2.word and j != i:
                word.count = word.count+wordv2.count
                words.pop(j)
    words = sorted(words, key=lambda word: word.count, reverse=True)
    return words
