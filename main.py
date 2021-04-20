from fastapi import FastAPI
import requests
import tweepy
app = FastAPI()

@app.get('/')
def index():
    return {'key':'value'}

# auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_token, access_token_secret)
# API Key 4d4KNhZxcj4IgrYSKO3KIUvJT
# API Secret Key: Z8L5wZFVnnqI2TZXIh1aFMvgHePAET9WDgEFPQOJ2BdWH0Kr3Q
# Bearer Token: AAAAAAAAAAAAAAAAAAAAAJfDNwEAAAAAJuncAKRJceeq5qGswCkcGEsHruQ%3Da9ZziGs2HB9meqMTSTdclW1MWSKxmaAh13jJ6NYwoBJM5xGCvO
# Access Token: 1245128680432709635-ha23ElSYEfG0C1S3mPO2yrt6WXAKNH
# Access Token Secret: psNmJDS4MikW6ICsFZlH292HzlE2sZbukXbO6y3OgsL4o
@app.get('/auth')
def oauth():
    auth = tweepy.OAuthHandler('4d4KNhZxcj4IgrYSKO3KIUvJT','Z8L5wZFVnnqI2TZXIh1aFMvgHePAET9WDgEFPQOJ2BdWH0Kr3Q')
    auth.set_access_token('1245128680432709635-ha23ElSYEfG0C1S3mPO2yrt6WXAKNH','psNmJDS4MikW6ICsFZlH292HzlE2sZbukXbO6y3OgsL4o')

    api = tweepy.API(auth)
    public_tweets = api.home_timeline()
    return api

@app.get('/rndtweets')
def tweets():
    api = oauth()
    public_tweets = api.home_timeline()
    for tweet in public_tweets:
        return(tweet.text)