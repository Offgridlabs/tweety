import os
from dotenv import load_dotenv
import tweepy
import time

# Load environment variables from .env file
load_dotenv()

# Get credentials from environment variables
api_key = os.getenv('API_KEY')
api_key_secret = os.getenv('API_KEY_SECRET')
access_token = os.getenv('ACCESS_TOKEN')
access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

# Authenticate to Twitter
auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)

# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True)

# Define the search term
search_words = "#Chelsea OR Chelsea OR #ChelseaFC OR #ChelseaFootballClub"

# Collect tweets
try:
    tweets = tweepy.Cursor(api.search_tweets, q=search_words, lang="en").items(5)

    for tweet in tweets:
        print(f"{tweet.user.name} said: {tweet.text}")
        try:
            # Retweet and like the tweet
            api.retweet(tweet.id)
            api.create_favorite(tweet.id)
        except tweepy.TweepyException as e:
            if hasattr(e, 'response') and e.response is not None:
                print(f"Error: {e.response.status_code} - {e.response.text}")
            else:
                print(f"Error: {e}")

except tweepy.TweepyException as e:
    if hasattr(e, 'response') and e.response is not None:
        print(f"Error: {e.response.status_code} - {e.response.text}")
    else:
        print(f"Error: {e}")

# Wait for 5 minutes before next action
time.sleep(300)