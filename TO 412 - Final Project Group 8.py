# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 13:46:46 2016

@author: michelkauffmann
"""
# get all mentions of tesla over the last 6 months
# need some sort of sentiment analysis on the tweets 
# analysis that leads to positive or negative scores for each tweet
# restrict tweeters to >5000 followers
# get stock prices/vol stats over the past 6 months
# join stock data and tweets data in SQL
# make some 'lit' visuals in Tableau   

# LOOP THROUGH USERS

#------------------------------------------------------------------------------
#              Disproving thet Tesla is a sentiment-driven stock
#------------------------------------------------------------------------------
import sys

sentimentData = 'wordwithStrength.txt'

def sentiment_dict(sentimentData):
    ''' (file) -> dictionary
This method should take your sentiment file
and create a dictionary in the form {word: value}
'''
    afinnfile = open(sentimentData)
    scores = {} # initialize an empty dictionary
    for line in afinnfile:
        term, score = line.split("\t") # The file is tab-delimited. "\t" means "tab character"
        scores[term] = float(score) # Convert the score to an integer.

    return scores # Print every (term, score) pair in the dictionary

#------------------------------------------------------------------------------

ConsumerKey = ""
ConsumerSecret = ""

import tweepy
import datetime, time
auth = tweepy.OAuthHandler(ConsumerKey, ConsumerSecret)
api = tweepy.API(auth)
sentiment = sentiment_dict(sentimentData)
analysis_tweets = []
influencers = ["eVehicle", "EVdotcom", "ev_perspective", "EVTweeter", "adamwerbach", "makower", "TeslaMotors", "elonmusk", "Jeremyclarkson", "evchels", "keith__johnston", "aminorjourney", "OEVAorg", "KenBurridge", "bobbyllew", "ChargePointnet", "ClimateCentral", "Greenpeace", "algore", "RnfrstAlliance", "sierraclub", "WWF", "sciam", "UNEP", "ClimateReality", "Earthjustice", "MilesGrant", "TeslaModelS", "TeslaMotorsClub", "TeslaRoadTrip", "Teslarati", "TheTeslaChannel", "teslaliving", "TeslaClubBE", "TeslaClubNL"]
means_tesla = ["tesla", "@teslamotors", "tsla", "model s", "model x"]
for user in influencers:
    max_tweets = 10000
    searched_tweets = []
    count_tweets = []
    unique_influencers = set([])
    last_id = -1
    new_tweets = []
    while len(searched_tweets) < max_tweets:
        count = max_tweets - len(searched_tweets)
        try:
            if len(new_tweets) == 0:
                new_tweets = api.user_timeline(user, count=count)
                searched_tweets.extend(new_tweets)
                last_id = new_tweets[-1].id
            else:
                new_tweets = api.user_timeline(user, count=count, max_id=str(last_id - 1))
                if not new_tweets:
                    break
                searched_tweets.extend(new_tweets)
                last_id = new_tweets[-1].id
        except tweepy.TweepError as e:
            break
    for tweet in searched_tweets:
        for word in means_tesla:
            if tweet.text.lower().count(word) > 0:
                tweet_word = tweet.text.lower().split()
                sent_score = 0
                date = tweet.created_at
                date = str(date)
                for word in tweet_word:
                    word = word.rstrip('?:!.,;"!@')
                    word = word.replace("\n", "")
                    
                    if word in sentiment.keys():
                        sent_score = sent_score + float(sentiment[word])
                            
                    else:
                        sent_score = sent_score                
                analysis_tweets.append({'user_screen_name':tweet.author.screen_name.encode('utf8'), 'created_at':date, 'sent_score':sent_score, 'followers_count':tweet.author.followers_count, 'retweet_count':tweet.retweet_count})

f_out=open("TeslaOutput2.csv", 'w')
f_out.write("user_screen_name, created_at, sent_score, followers_count, retweet_count\n")
for tweet in analysis_tweets:
    f_out.write(tweet['user_screen_name']+","+str(tweet['created_at'])+","+str(tweet['sent_score'])+","+str(tweet['followers_count'])+","+str(tweet['retweet_count'])+"\n")
f_out.close()    