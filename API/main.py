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
API_Secret_Key = 'bZNftO5qycR8vmMb9xefCZNsmydVymIeP8pDuCWJDbr3QfEh0x'
Bearer_Token = 'AAAAAAAAAAAAAAAAAAAAAJfDNwEAAAAAYAY3Su%2BcII9eJhkq9QHbI0vFhqw%3Dzdc6QSmR3gZXs4hVDb8mEslz5oB7xsUDbINuD70bVoV1s0c2j8'
Access_Token = '1245128680432709635-Sa3SU1EZdNaJxOM987kYzbMMPg5SDY'
Access_Token_Secret = 'jzAqqssWb85AeH5CWQflH3v1dblW9W1qSdnU2c0aCTqpt'
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

