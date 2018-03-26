
import tweepy
from secrets import *


class  PoopTweet():

	def __init__(self):

		pass

	def send_tweet(self,tweet_text):

		#Construct the tweepy object for tweeting
		auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
		auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
		tweet = tweepy.API(auth)

		tweet.update_status(tweet_text)

	def send_tweet_with_media(self,filename,tweet_text=''):


		#Construct the tweepy object for tweeting
		auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
		auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
		tweet = tweepy.API(auth)
		tweet.update_with_media(filename,tweet_text)
