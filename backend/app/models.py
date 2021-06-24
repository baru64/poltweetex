from sqlalchemy import Column, Integer, String

from .database import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)

class Party(Base):
    __tablename__ = "parties"

    id = Column(Integer, primary_key=True, index= True)
    name = Column(String, index= True)

class Politician(Base):
    __tablename__ = "politicians"

    id = Column(Integer, primary_key=True, index=True)
    twitter_ID = Column(String, index=True)
    party_ID = Column(Integer,index=True)


class Word(Base):
    __tablename__="words"

    id = Column(Integer, primary_key=True, index=True)
    word = Column(String, index=True)
    politician_id = Column(Integer, index=True)
    tweet_id = Column(String, index=True)
    count = Column(Integer,index=True)


class WordIndex(Base):
    __tablename__ = "wordIndexes"

    id = Column(Integer, primary_key=True, index=True)
    word = Column(String, index=True)

