from os import listdir
from json import loads, JSONDecodeError

USER = 'barackobama'
FRIENDS = ['barackobama', 'OFA','VP']

ANALYSES_FOLDER = 'analyses/'
TWEETS_FOLDER = 'tweets/'

tweet_scores_per_model = {}
all_tweets = set()

for filename in listdir(ANALYSES_FOLDER):

	username, model = filename.split('.')

	if username != USER or '_' in model:
		continue

	original_tweets = open(TWEETS_FOLDER+username+'.txt').readlines()

	tweet_scores_per_model[model] = []

	for predictions,tweet in zip(open(ANALYSES_FOLDER+filename),original_tweets):

		tweet = tweet.strip()
		all_tweets.add(tweet)
		correct = 0
		total = 0

		try:
			predictions = loads(predictions)
		except JSONDecodeError:
			continue

		current_word = ''
		current_tweet = ''

		for character,prediction in zip(tweet,[[]]+predictions):

			try:
				predicted_word = prediction[0][0]
			except IndexError:
				try:
					predicted_word = prediction[1][0]
				except IndexError:
					predicted_word = None

			if character == ' ':
				current_word = ''
			else:
				current_word += character

			current_tweet += character

			if predicted_word == None or len(predicted_word) < len(current_word):
				predicted_character = None
			else:
				predicted_character = predicted_word[len(current_word)-1]

			if character in [' ',''] or len(current_tweet) < 2:
				pass
			else:
				total += 1

				if predicted_character != None and character == predicted_character:
					correct += 1

		try:
			tweet_scores_per_model[model].append(correct/total)
		except ZeroDivisionError:
			tweet_scores_per_model[model].append(0)

all_tweet_info = []

for n,tweet in enumerate(all_tweets):

	cumulative_friend_rank = 0
	scores = []

	for model, tweet_scores in tweet_scores_per_model.items():

		try:
			scores.append((model,tweet_scores[n]))
		except IndexError:
			#print(model,len(tweet_scores),n)
			continue;

	scores = sorted(scores,key=lambda x: x[1], reverse=True)

	for rank, (model, tweet_score) in enumerate(scores):

		if model in FRIENDS:
			cumulative_friend_rank += rank

	all_tweet_info.append({'content':tweet, 'scores': scores, 'cumulative_friend_rank': cumulative_friend_rank})

all_tweet_info = sorted(all_tweet_info, key = lambda x: x['cumulative_friend_rank'], reverse=True)

for tweet_info in all_tweet_info:

	if 'http' in tweet_info['content'] or '&amp;' in tweet_info['content'] or '@' in tweet_info['content'] or 'President Obama' in tweet_info['content']:
		continue

	print(tweet_info['content'])
	print(tweet_info['scores'])
	print()