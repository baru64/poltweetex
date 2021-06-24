from fastapi import FastAPI, Query
import tweepy
import configparser
import string
from typing import List

config = configparser.ConfigParser()
config.read('config.ini')

app = FastAPI()

auth = tweepy.OAuthHandler(
    config['twitter']['API_Key'], config['twitter']['API_Secret_Key'])
auth.set_access_token(config['twitter']['Access_Token'],
                      config['twitter']['Access_Token_Secret'])
api = tweepy.API(auth)


@app.get('/rndtweets')
def tweets():
    public_tweets = api.home_timeline()
    response = {}
    i = 0
    for tweet in public_tweets:
        i += 1
        print(tweet.text)
        response[i] = tweet.text
    return response


@app.get('/users/{userName}')
def getUserId(userName):
    response = api.get_user(userName)
    return {userName: response.id}


@app.get('/users/{userName}/tweets')
def getUserTweets(userName):
    response = {}
    userId = getUserId(userName)[userName]
    print(userId)
    tweets = api.user_timeline(user_id=userId,
                               count=10,
                               include_rts=False,
                               tweet_mode='extended'
                               )
    for info in tweets:
        response[info.id] = info.full_text
    return response

# Tutaj chce mieć przykłąd funkcji która potem będzie użyta w Azure.


class Tweet:
    def __init__(self, id, createdAt, text, wordCount):
        self.id = id
        self.createdAt = createdAt
        self.text = text
        self.wordCount = wordCount

    def __str__(self):
        return f'Tweet class: \n[Id: {self.id} \nCreated At: {self.createdAt}\nText: {self.text}\nWordCount: {self.wordCount}]'


def replaceUnwantedSigns(sentence):
    polishSigns = {'ą': 'a', 'ć': 'c', 'ę': 'e', 'ł': 'l', 'ń': 'n',
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

# Wersja dla jednego usera


@app.get("/users/{userId}/toDB")
def analyzeUserTweets(userId):
    tweets = api.user_timeline(user_id=userId,
                               count=10,
                               include_rts=False,
                               tweet_mode='extended')
    response = []
    for tweet in tweets:
        tweet.full_text = simplifyTweetText(tweet.full_text)
        dict = mapReducer(tweet.full_text)
        response.append(
            Tweet(tweet.id, tweet.created_at, tweet.full_text, dict))

    return response

# Wersja dla listy userów


@app.get("/toDB")
def analyzeUserTweets(usersIds: List[str] = Query(None)):
    response = []
    for userId in usersIds:
        tweets = api.user_timeline(user_id=userId,
                                   count=10,
                                   include_rts=False,
                                   tweet_mode='extended')
        userResposne = []
        for tweet in tweets:
            tweet.full_text = simplifyTweetText(tweet.full_text)
            dict = mapReducer(tweet.full_text)
            userResposne.append(
                Tweet(tweet.id, tweet.created_at, tweet.full_text, dict))
        response.append(userResposne)
    print(response)
    return response
