from sqlalchemy import Column, String, Integer, Date, ForeignKey

from .database import Base


class Party(Base):
    __tablename__ = "parties"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    politicians = relationship("Politician", back_populates="party")

class Politician(Base):
    __tablename__ = "politicians"

    id = Column(Integer, primary_key=True, index=True)
    twitter_id = Column(String)
    last_update = Column(Date)
    party_id = Column(Integer, ForeignKey("party.id"))

    party = relationship("Party", back_populates="politicians")
    words = relationship("Word", back_populates="politician")

class Word(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    word = Column(String)
    politician_id = Column(Integer, ForeignKey("politicians.id"))
    count = Column(Integer)

    politician = relationship("Politician", back_populates="words")


class WordIndex(Base):
    __tablename__ = "wordindex"

    word = Column(String, primary_key=True, index=True)
