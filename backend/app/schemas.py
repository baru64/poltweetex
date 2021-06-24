from pydantic import BaseModel

# Party schema


class PartyBase(BaseModel):
    name: str


class PartyCreate(PartyBase):
    pass


class Party(PartyBase):
    id: int

    class Config:
        orm_mode = True

# Politicians schema


class PoliticianBase(BaseModel):
    name: str
    twitter_id: str
    party_id: int
    last_update: str


class PoliticianCreate(PoliticianBase):
    pass


class Politician(PoliticianBase):
    class Config:
        orm_mode = True

# Word schema


class WordBase(BaseModel):
    word: str
    politician_id: str
    tweet_id: str
    count: int


class WordCreate(WordBase):
    pass


class Word(WordBase):
    id: int

    class Config:
        orm_mode = True

# WrodIndex schema


class WordIndexBase(BaseModel):
    word: str


class WordIndexCreate(WordIndexBase):
    pass


class WordIndex(WordIndexBase):
    id: int

    class Config:
        orm_mode = True
