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
CHOSEN_TWEETS = {'barackobama':[(407,'748958754020790272'),(2692,'519190672251686912'),(74,'863756100948156416'),(26,'952914779458424832'),(1245,'650041294798983168')],
				'ladygaga':[(1115,'742537484379136000'),(2022,'542455766561468420'),(1474,'643999055052300288'),(1701,'608364277431468032'),(1336,'674952742813736960')],
				'jtimberlake':[(1922,'317033714838286336'),(2102,'275158352978386945'),(1479,'401614200638013440'),(1075,'523624551838519296'),(159,'955826144502218754')],
				'kimkardashian':[(1183,'967031272278188033'),(608,'989227725935144961'),(340,'1004412177376333829'),(1908,'925595030340771840'),(1176,'967479788347600896')]}

TWEETS_FOLDER = 'research/tweets/'
ANALYSIS_FOLDER = 'research/analyses/'
SCORES_FILE = 'scores_v2'
OUTPUT_FOLDER = 'js/'

#Declare some dictionaries, keys will be added dynamically later
example_tweets = {}
eval_scores_per_language_model = {}
sociolect_scores_per_language_model = {}
predictions_per_language_model = {}
scores_per_tweet = {}

# Already load in some info
users_and_friends = {'barackobama':['VP'],
					 'jtimberlake':['ChrisStapleton','AnnaKendrick47','jimmyfallon'],
					 'kimkardashian':['khloekardashian','MakeupByMario'],
					 'ladygaga':['itstonybennett','MarkRonson','faspiras']
					}

all_scores = {line.split()[0]: float(line.split()[1]) for line in open(SCORES_FILE)}

#Iterate over all users
for user, tweet_ids in CHOSEN_TWEETS.items():

	#Add keys to dict
	example_tweets[user] = []
	eval_scores_per_language_model[user] = []
	sociolect_scores_per_language_model[user] = []
	predictions_per_language_model[user] = {}
	scores_per_tweet[user] = []

	#Get all tweets for this user
	all_tweets = open(TWEETS_FOLDER+user+'.txt').readlines()

	#Save the chosen tweets
	for tweet_index, tweet_id in tweet_ids:
		tweet_index -= 1 #Index taken manually from line numbers

		example_tweets[user].append(all_tweets[tweet_index])
		scores_per_tweet[user].append({'id':tweet_id,'predicted_by':{}})

	#Go over all models that predicted things for this user
	for model in list(users_and_friends.keys()) + users_and_friends[user]:

		#Get the score from a separate output file
		predictions_per_language_model[user][model] = []
		sociolect_scores_per_language_model[user].append((model,round(100*all_scores[user+'.'+model])))

		if model in users_and_friends.keys():
			eval_scores_per_language_model[user].append((model,round(100*all_scores[user+'.'+model])))

		#Collect all analyses for this user model combi
		all_analyses = open(ANALYSIS_FOLDER+user+'.'+model).readlines()

		#Go over all example tweets
		for n, (tweet_index, tweet_id) in enumerate(tweet_ids):
			tweet_index -= 1 #Index taken manually from line numbers

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

	#Sort the model scores
	eval_scores_per_language_model[user].sort(key=lambda x: x[1],reverse=True)
	sociolect_scores_per_language_model[user].sort(key=lambda x: x[1],reverse=True)

#Output all the collected data in json
open(OUTPUT_FOLDER+'example_tweets.js','w').write('var example_tweets = '+dumps(example_tweets))
open(OUTPUT_FOLDER+'eval_scores_per_language_model.js','w').write('var eval_scores_per_language_model = '+dumps(eval_scores_per_language_model))
open(OUTPUT_FOLDER+'sociolect_scores_per_language_model.js','w').write('var sociolect_scores_per_language_model = '+dumps(sociolect_scores_per_language_model))
open(OUTPUT_FOLDER+'predictions_per_language_model.js','w').write('var predictions_per_language_model = '+dumps(predictions_per_language_model))
open(OUTPUT_FOLDER+'scores_per_tweet.js','w').write('var scores_per_tweet = '+dumps(scores_per_tweet))