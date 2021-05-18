from fastapi import FastAPI
import requests
import tweepy
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
print('API_Key' in  config)


app = FastAPI()

@app.get('/')
def index():
    return {'key':'value'}


@app.get('/auth')
def oauth():
    auth = tweepy.OAuthHandler('API_Key' in config,'API_Secret_Key' in config)
    auth.set_access_token('Access_Token' in config)

    api = tweepy.API(auth)
    public_tweets = api.home_timeline()
    return api


@app.get('/rndtweets')
def tweets():
    api = oauth()
    public_tweets = api.home_timeline()
    for tweet in public_tweets:
        return(tweet.text)

