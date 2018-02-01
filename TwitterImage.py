from tweepy import *
from tweepy import OAuthHandler
import json
from PIL import Image
import requests
from io import BytesIO
import numpy as np
from SimpleCV import Image as simpleIm
import random


class TwitterConnection:
    def __init__(self):
        self.consumer_key = ''
        self.consumer_secret = ''
        self.access_token = ''
        self.access_secret = ''
        self.auth = OAuthHandler(self.consumer_key, self.consumer_secret)
        self.auth.set_access_token(self.access_token, self.access_secret)
        self.api = API(self.auth)
        self.recentImage = None
        self.recentTweetText = ""
        self.recentImageURLS = []
        self.tweets = []
        self.updateTweetsAndMedia()

    def getRecentImage(self):
        return self.recentImage

    def setRecentImage(self, img):
        self.recentImage = img

    def getRandomRecentImage(self, returnImage=None):
        if len(self.tweets == 0): self.tweets = self.getMentionedTweetsWithMedia()
        if len(self.tweets) > 0:
            imgIndex = random.randint(0, len(self.tweets))
            tweeted_image = self.recentImageURLS[imgIndex][-1]
            response = requests.get(tweeted_image)
            img = Image.open(BytesIO(response.content))
            img_data = np.array(img)
            simpleCVImage = simpleIm(img_data)
            if (not returnImage == None):
                returnImage[0] = simpleCVImage
            return simpleCVImage
        else:
            return []

    def getMentionedTweetsWithMedia(self, tweet_count=10):
        tweets = self.api.mentions_timeline(count=tweet_count)
        outtweets = []  # initialize master list to hold our ready tweets
        for tweet in tweets:
            # not all tweets will have media url, so lets skip them
            try:
                print tweet.entities['media'][0]['media_url']
            except (NameError, KeyError):
                # we dont want to have any entries without the media_url so lets do nothing
                pass
            else:
                # got media_url - means add it to the output
                outtweets.append(
                    [tweet.id_str, tweet.created_at, tweet.text.encode("utf-8"),
                     tweet.entities['media'][0]['media_url']])
        print(outtweets)
        return outtweets

    def getMentionedTweets(self, tweet_count=10):
        tweets = self.api.mentions_timeline(count=tweet_count)

        outtweets = []  # initialize master list to hold our ready tweets
        for tweet in tweets:
            # not all tweets will have media url, so lets skip them
            media_url = ""
            try:
                media_url = tweet.entities['media'][0]['media_url']
            except (NameError, KeyError):
                # we dont want to have any entries without the media_url so lets do nothing
                pass
            outtweets.append(
                [tweet.id_str, tweet.created_at, tweet.text.encode("utf-8"),
                 media_url])

        return outtweets

    def getTopPhoto(self, returnImage=None):
        self.tweets = self.getMentionedTweetsWithMedia()
        if len(self.tweets) > 0:
            self.recentImageURLS = self.tweets
            tweeted_image = self.tweets[0][-1]
            response = requests.get(tweeted_image)
            img = Image.open(BytesIO(response.content))
            img_data = np.array(img)
            simpleCVImage = simpleIm(img_data)
            if (not returnImage == None):
                returnImage = [simpleCVImage]
            return simpleCVImage
        else:
            return []

    def getTopPhotoFromRecentTweets(self):
        if len(self.tweets) > 0:
            tweeted_image = self.tweets[0][-1]
            if len(tweeted_image) > 0:
                response = requests.get(tweeted_image)
                img = Image.open(BytesIO(response.content))
                self.recentImage = simpleIm(np.array(img))
                return

        self.recentImage = None

    def getRecentTweetText(self):
        for tweet in self.tweets:
            if len(tweet[2]) > 0:
                self.recentTweetText = tweet[2]
                return

        self.recentTweetText = ""
        return

    def updateTweetsAndMedia(self):
        print("UPDATING TWITTER MEDIA MENTIONS")
        self.tweets = self.getMentionedTweets()
        self.getTopPhotoFromRecentTweets()
        self.getRecentTweetText()
