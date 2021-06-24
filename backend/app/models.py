from sqlalchemy import Column, Integer, String, DateTime

from .database import Base


class Party(Base):
    __tablename__ = "parties"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)


class Politician(Base):
    __tablename__ = "politicians"

    twitter_id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    party_id = Column(Integer, index=True)
    last_update = Column(DateTime, index=True)


class Word(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True, index=True)
    word = Column(String, index=True)
    politician_id = Column(String, index=True)
    tweet_id = Column(String, index=True)
    count = Column(Integer, index=True)
    date = Column(DateTime, index=True)


class WordIndex(Base):
    __tablename__ = "wordIndexes"

    id = Column(Integer, primary_key=True, index=True)
    word = Column(String, index=True)
