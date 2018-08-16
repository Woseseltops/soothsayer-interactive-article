from os import listdir
from json import loads, JSONDecodeError

ANALYSES_FOLDER = 'analyses/'
TWEETS_FOLDER = 'tweets/'

for filename in listdir(ANALYSES_FOLDER):

	username = filename.split('.')[0]
	original_tweets = open(TWEETS_FOLDER+username+'.txt').readlines()

	correct = 0
	total = 0

	for predictions,tweet in zip(open(ANALYSES_FOLDER+filename),original_tweets):

		tweet = tweet.strip()

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
		print(filename,correct/total)
	except ZeroDivisionError:
		print(filename,'problem')