import tweepy
import string
import os


from . import models
from .database import SessionLocal

# INDEX = int(os.environ['JOB_COMPLETION_INDEX'])


auth = tweepy.OAuthHandler(os.environ['API_Key'], os.environ['API_Secret_Key'])
auth.set_access_token(os.environ['Access_Token'],
                      os.environ['Access_Token_Secret'])

twitterAPI = tweepy.API(auth)


def main():
    with SessionLocal() as db:
        politicians = db.query(models.Politician).all()
        for politician in politicians:
            print("Reading tweets of "+politician.name)
            twitts = twitterAPI.user_timeline(user_id=politician.twitter_id,
                                              count=10,
                                              include_rts=False,
                                              tweet_mode='extended'
                                              )
            print("Analizing tweets of "+politician.name)
            for info in reversed(twitts):
                if(info.created_at > politician.last_update):
                    politician.last_update = info.created_at
                    db.add(politician)
                else:
                    continue
                info.full_text = simplifyTweetText(info.full_text)
                dict = mapReducer(info.full_text)
                for key in dict:
                    new_word = models.Word(
                        word=key,
                        politician_id=politician.twitter_id,
                        tweet_id=info.id,
                        count=dict[key],
                        date=info.created_at
                    )
                    db.add(new_word)
        db.commit()


def replaceUnwantedSigns(sentence):
    polishSigns = {'ą': 'a', 'ć': 'c', 'ę': 'e', 'ł': 'l', 'ń': 'n', '…': '',
                   'ó': 'o', 'ś': 's', 'ż': 'z', 'ź': 'z', '”': '', "„": ""}
    sentence = sentence.translate(str.maketrans('', '', string.punctuation))
    for sign in polishSigns:
        sentence = sentence.replace(sign, polishSigns[sign])
    return sentence


def removePutationMarks(sentence):
    sentence = sentence.translate(str.maketrans('', '', string.punctuation))
    return sentence


def simplifyTweetText(sentence):
    sentence = replaceUnwantedSigns(sentence)
    sentence = removePutationMarks(sentence)
    return sentence


def mapReducer(text):
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
    main()
