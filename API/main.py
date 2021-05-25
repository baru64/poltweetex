from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
import requests
import tweepy
import configparser
import json

config = configparser.ConfigParser()
config.read('config.ini')

app = FastAPI()

auth = tweepy.OAuthHandler(config['twitter']['API_Key'], config['twitter']['API_Secret_Key' ])
auth.set_access_token(config['twitter']['Access_Token'],config['twitter']['Access_Token_Secret'])
api = tweepy.API(auth)

@app.get('/rndtweets')
def tweets():
    public_tweets = api.home_timeline()
    response={}
    i=0
    for tweet in public_tweets:
        i+=1
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
                            include_rts = False,
                            tweet_mode = 'extended'
                            )
    for info in tweets:
        response[info.id] = info.full_text
    return response