import tweepy
import string
import os
import json
from typing import List, Dict
import logging
import sys

from . import models
from .database import SessionLocal, engine


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)

auth = tweepy.OAuthHandler(
    os.getenv('API_Key'),
    os.getenv('API_Secret_Key')
)
auth.set_access_token(
    os.getenv('Access_Token'),
    os.getenv('Access_Token_Secret')
)

twitterAPI = tweepy.API(auth)


def setupDB():
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)

    with open("/etc/config/parties.json", 'r') as politicians_json:
        parties = json.load(politicians_json)
    with SessionLocal() as db:
        for party in parties:
            if db.query(models.Party).get(party["party_ID"]) is None:
                new_party = models.Party(
                    id=party["party_ID"],
                    name=party['Party']
                )
                db.add(new_party)
            for politician in party["Politicians"]:
                if db.query(models.Politician).get(politician["ID"]) is None:
                    new_politician = models.Politician(
                        twitter_id=politician['ID'],
                        name=politician['Name'],
                        party_id=party["party_ID"],
                        last_since_id=None
                    )
                    db.add(new_politician)
        db.commit()


def main():
    with SessionLocal() as db:
        politicians: List[models.Politician] = db.query(
            models.Politician).all()
        for politician in politicians:
            logger.debug(f"Reading {politician.name} tweets")
            tweets = None
            if politician.last_since_id is None:
                tweets = twitterAPI.user_timeline(
                    user_id=politician.twitter_id,
                    count=10000,
                    include_rts=False,
                    tweet_mode='extended'
                )
            else:
                tweets = twitterAPI.user_timeline(
                    user_id=politician.twitter_id,
                    since_id=politician.last_since_id,
                    include_rts=False,
                    tweet_mode='extended'
                )
            logger.debug(f"Analyzing {politician.name} tweets")
            # set new last id
            politician.last_since_id = tweets[0].id
            db.add(politician)
            for tweet in tweets:
                tweet.full_text = simplifyTweetText(tweet.full_text)
                words = mapReducer(tweet.full_text)
                for word, count in words.items():
                    new_word = models.Word(
                        word=word,
                        politician_id=politician.twitter_id,
                        tweet_id=tweet.id,
                        count=count,
                        date=tweet.created_at
                    )
                    db.add(new_word)
        db.commit()


def replaceUnwantedSigns(sentence: str) -> str:
    polishSigns = {'ą': 'a', 'ć': 'c', 'ę': 'e', 'ł': 'l', 'ń': 'n', '…': '',
                   'ó': 'o', 'ś': 's', 'ż': 'z', 'ź': 'z', '”': '', "„": ""}
    sentence = sentence.translate(str.maketrans('', '', string.punctuation))
    for sign in polishSigns:
        sentence = sentence.replace(sign, polishSigns[sign])
    return sentence


def removePutationMarks(sentence: str) -> str:
    sentence = sentence.translate(str.maketrans('', '', string.punctuation))
    return sentence


def simplifyTweetText(sentence: str) -> str:
    sentence = replaceUnwantedSigns(sentence)
    sentence = removePutationMarks(sentence)
    return sentence


def mapReducer(text) -> Dict:
    words = text.split(' ')
    wordsDict = {}
    for word in words:
        if word == "":
            continue
        if word in wordsDict:
            wordsDict[word] = wordsDict[word]+1
        else:
            wordsDict[word.lower()] = 1
    return wordsDict


if __name__ == "__main__":
    if os.getenv("SETUP_DB", "false") == "true":
        setupDB()
    main()
