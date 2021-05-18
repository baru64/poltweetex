from fastapi import FastAPI
import requests
import tweepy
import configparser


config = configparser.ConfigParser()
config.read('config.ini')

print(config['twitter']['Access_Token'])
print(config['twitter']['API_Key'])
print(config['twitter']['API_Secret_Key'])
print(config['twitter']['Access_Token_Secret'])

app = FastAPI()

@app.get('/')
def index():
    return {'key':'value'}

@app.get('/auth')
def oauth():
    auth = tweepy.OAuthHandler(config['twitter']['API_Key'], config['twitter']['API_Secret_Key' ])
    auth.set_access_token(config['twitter']['Access_Token'], config['twitter']['Access_Token_Secret'])
    api = tweepy.API(auth)
    public_tweets = api.home_timeline()
    return api

@app.get('/rndtweets')
def tweets():
    api = oauth()
    public_tweets = api.home_timeline()
    for tweet in public_tweets:
        return(tweet.text)

