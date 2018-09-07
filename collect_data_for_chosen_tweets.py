from json import loads, dumps

def compare_tweet_to_predictions(tweet,predictions):

	correct = 0
	total = 0

	current_word = ''
	current_tweet = ''

	annotated_tweet = ''

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
			annotated_tweet += character
			pass
		else:
			total += 1

			if predicted_character != None and character == predicted_character:
				correct += 1
				annotated_tweet += "<span class='correct_char'>"+character+'</span>'
			else:
				annotated_tweet += character

	try:
		return correct/total, annotated_tweet
	except:
		print(tweet,predictions)

#Static parameters
CHOSEN_TWEETS = {'barackobama':[(0,'a'),(1,'b'),(2,'c'),(3,'d'),(4,'e')],
				'jtimberlake':[(0,'a'),(1,'b'),(2,'c'),(3,'d'),(4,'e')],
				'kimkardashian':[(0,'a'),(1,'b'),(2,'c'),(3,'d'),(4,'e')],
				'ladygaga':[(0,'a'),(1,'b'),(2,'c'),(3,'d'),(4,'e')]}

TWEETS_FOLDER = 'research/tweets/'
ANALYSIS_FOLDER = 'research/analyses/'
SCORES_FILE = 'latest_scores'
OUTPUT_FOLDER = 'js/'

#Declare some dictionaries, keys will be added dynamically later
example_tweets = {}
scores_per_language_model = {}
predictions_per_language_model = {}
scores_per_tweet = {}

# Already load in some info
all_users = ['barackobama','jtimberlake','kimkardashian','ladygaga'] #list(CHOSEN_TWEETS.keys())
all_scores = {line.split()[0]: float(line.split()[1]) for line in open(SCORES_FILE)}

#Iterate over all users
for user, tweet_ids in CHOSEN_TWEETS.items():

	#Add keys to dict
	example_tweets[user] = []
	scores_per_language_model[user] = []
	predictions_per_language_model[user] = {}
	scores_per_tweet[user] = []

	#Get all tweets for this user
	all_tweets = open(TWEETS_FOLDER+user+'.txt').readlines()

	#Save the chosen tweets
	for tweet_index, tweet_id in tweet_ids:
		example_tweets[user].append(all_tweets[tweet_index])
		scores_per_tweet[user].append({'id':tweet_id,'predicted_by':{}})

	#Go over all models that predicted things for this user
	for model in all_users:

		#Get the score from a separate output file
		scores_per_language_model[user].append((model,round(100*all_scores[user+'.'+model])))
		predictions_per_language_model[user][model] = []

		#Collect all analyses for this user model combi
		all_analyses = open(ANALYSIS_FOLDER+user+'.'+model).readlines()

		#Go over all example tweets
		for n, (tweet_index, tweet_id) in enumerate(tweet_ids):

			all_predictions_for_tweet = []			
			current_tweet = example_tweets[user][n]
			current_analysis = loads(all_analyses[tweet_index])

			#Interpret the predictions for this tweet model combi
			for knn_predictions, freq_predictions in current_analysis:
				current_predictions = knn_predictions

				for freq_prediction in freq_predictions:

					if len(current_predictions) == 3:
						break

					current_predictions.append(freq_prediction)

				all_predictions_for_tweet.append(current_predictions)

			predictions_per_language_model[user][model].append(all_predictions_for_tweet)

			score, annotated_tweet = compare_tweet_to_predictions(current_tweet,current_analysis)
			scores_per_tweet[user][n]['predicted_by'][model] = {'text':annotated_tweet,'score':round(100*score)}

#Output all the collected data in json
open(OUTPUT_FOLDER+'example_tweets.js','w').write('var example_tweets = '+dumps(example_tweets))
open(OUTPUT_FOLDER+'scores_per_language_model.js','w').write('var scores = '+dumps(scores_per_language_model))
open(OUTPUT_FOLDER+'predictions_per_language_model.js','w').write('var predictions_per_language_model = '+dumps(predictions_per_language_model))
open(OUTPUT_FOLDER+'scores_per_tweet.js','w').write('var scores_per_tweet = '+dumps(scores_per_tweet))