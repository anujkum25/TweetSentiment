# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 15:19:05 2019

@author: I345144
"""

import re 
import tweepy 
from tweepy import OAuthHandler 
from textblob import TextBlob 
from wordcloud import WordCloud, STOPWORDS 
import matplotlib.pyplot as plt
import pandas as pd

import os
## change path for your system
path="C:\\Users\\i345144\\OneDrive\\Documents\\MSRUS\\Data Mining and Analytics\\Assignment"
os.chdir(path)

class TwitterClient(object):
	''' 
	Generic Twitter Class for sentiment analysis. 
	'''
	def __init__(self): 
		''' 
		Class constructor or initialization method. 
		'''
		# keys and tokens from the Twitter Dev Console 
		consumer_key = 'put_your_key_here'
		consumer_secret = 'put_your_consumer_secret_here'
		access_token = 'put_your_access_token_here'
		access_token_secret = 'put_your_access_token_secret_here'





		# attempt authentication 
		try: 
			# create OAuthHandler object 
			self.auth = OAuthHandler(consumer_key, consumer_secret) 
			# set access token and secret 
			self.auth.set_access_token(access_token, access_token_secret) 
			# create tweepy API object to fetch tweets 
			self.api = tweepy.API(self.auth) 
		except: 
			print("Error: Authentication Failed") 

	def clean_tweet(self, tweet): 
		''' 
		Utility function to clean tweet text by removing links, special characters 
		using simple regex statements. 
		'''
		return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
								 

	def get_tweet_sentiment(self, tweet): 
		''' 
		Utility function to classify sentiment of passed tweet 
		using textblob's sentiment method 
		'''
		# create TextBlob object of passed tweet text 
		analysis = TextBlob(self.clean_tweet(tweet)) 
		# set sentiment 
		if analysis.sentiment.polarity > 0: 
			return 'positive'
		elif analysis.sentiment.polarity == 0: 
			return 'neutral'
		else: 
			return 'negative'

	def get_tweets(self, query, count = 10): 
		''' 
		Main function to fetch tweets and parse them. 
		'''
		# empty list to store parsed tweets 
		tweets = [] 

		try: 
			# call twitter api to fetch tweets 
			fetched_tweets = self.api.search(q = query, count = count) 

			# parsing tweets one by one 
			for tweet in fetched_tweets: 
				# empty dictionary to store required params of a tweet 
				parsed_tweet = {} 

				# saving text of tweet 
				parsed_tweet['text'] = tweet.text 
				# saving sentiment of tweet 
				parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text) 

				# appending parsed tweet to tweets list 
				if tweet.retweet_count > 0: 
					# if tweet has retweets, ensure that it is appended only once 
					if parsed_tweet not in tweets: 
						tweets.append(parsed_tweet) 
				else: 
					tweets.append(parsed_tweet) 

			# return parsed tweets 
			return tweets 

		except tweepy.TweepError as e: 
			# print error (if any) 
			print("Error : " + str(e))

	def word_cloud (self, tweet):
		comment_words = ' '
		stopwords = set(STOPWORDS)
		
		df= pd.DataFrame(tweet)
		#print("This is df:", df)
		#df.to_csv("tweets.csv", sep='\t')
		
		for val in df.text: 
			# typecaste each val to string 
			val = str(val) 
			  
			# split the value 
			tokens = val.split() 
				  
			# Converts each token into lowercase 
			for i in range(len(tokens)): 
				tokens[i] = tokens[i].lower() 
					  
			for words in tokens: 
				comment_words = comment_words + words + ' '
			  
			  
			wordcloud = WordCloud(width = 800, height = 800, 
							background_color ='white', 
							stopwords = stopwords, 
							min_font_size = 10).generate(comment_words) 
			  
			# plot the WordCloud image                        
			plt.figure(figsize = (8, 8), facecolor = None) 
			plt.imshow(wordcloud) 
			plt.axis("off") 
			plt.tight_layout(pad = 0) 
			plt.savefig('word_cloud.png')
  
			plt.show() 
            

def main(): 
	# creating object of TwitterClient Class 
	api = TwitterClient() 
	# calling function to get tweets 
  # provide a topic on which you want to extract tweets, for my case it is Article 370
	tweets = api.get_tweets(query = 'Article 370', count = 2000) 
    
	# picking positive tweets from tweets 
	ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive'] 
	# percentage of positive tweets 
	print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets))) 
	# picking negative tweets from tweets 
	ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative'] 
	# percentage of negative tweets 
	print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets))) 
	# percentage of neutral tweets 
	print("Neutral tweets percentage: {} % \ ".format(100*(len(tweets) - len(ntweets) -len(ptweets))/len(tweets)))
    
	api.word_cloud(ptweets)
    
	# printing first 5 positive tweets 
	print("\n\nPositive tweets:") 
	for tweet in ptweets[:10]: 
		print(tweet['text']) 

	# printing first 5 negative tweets 
	print("\n\nNegative tweets:") 
	for tweet in ntweets[:10]: 
		print(tweet['text']) 
    
    

if __name__ == "__main__": 
	# calling main function 
	main() 
