from os import listdir

TWEETS_FOLDER = 'tweets/'

nr_of_tweets = []

for twitter_user in listdir(TWEETS_FOLDER):
	nr_of_tweets.append((twitter_user,len(open(TWEETS_FOLDER+twitter_user).readlines())))

for twitter_user, nr_of_tweets in sorted(nr_of_tweets,key=lambda x: x[1]):
	print(twitter_user,nr_of_tweets)