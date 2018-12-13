from make_predictions_from_model import get_instances_for_twitter_user
from json import dumps

def ongoing_text_to_features(text,nr_of_features):

	result = []

	text_so_far = ''
	current_word = ''

	for character in text:

		#Administration about the text so far
		text_so_far += character
		current_word += character
		words_so_far = text_so_far.split()

		if character != ' ':
			words_so_far = words_so_far[:-1]
		else:
			current_word = ''

		#Prepare the the info for a classifier predction
		features = words_so_far[-nr_of_features:]

		while len(features) < nr_of_features:
			features = ['_'] + features

		result.append(features)

	return result

#========================

TWEETS_FOLDER = 'tweets/'
NR_OF_FEATURES = 3

CHOSEN_TWEETS = {'barackobama':[(407,'748958754020790272'),(2692,'519190672251686912'),(74,'863756100948156416'),(26,'952914779458424832'),(1245,'650041294798983168')],
				'ladygaga':[(1115,'742537484379136000'),(2022,'542455766561468420'),(1474,'643999055052300288'),(1701,'608364277431468032'),(1336,'674952742813736960')],
				'jtimberlake':[(1922,'317033714838286336'),(2102,'275158352978386945'),(1479,'401614200638013440'),(1075,'523624551838519296'),(159,'955826144502218754')],
				'kimkardashian':[(1183,'967031272278188033'),(608,'989227725935144961'),(340,'1004412177376333829'),(1908,'925595030340771840'),(1176,'967479788347600896')]}

OUTPUT_FILE = 'nearest_neighbors.js'

result = {}

for twitter_user, tweets in CHOSEN_TWEETS.items():
	
	print(twitter_user)
	result[twitter_user] = []

	#Collect the 'training material' for this user
	instances = get_instances_for_twitter_user(twitter_user,NR_OF_FEATURES)

	for tweet_index, tweet_id in tweets:

		best_trigrams_for_tweet = []

		#Collect the current tweet
		tweet_text = open(TWEETS_FOLDER+twitter_user+'.txt').readlines()[tweet_index-1]
		features = ongoing_text_to_features(tweet_text,NR_OF_FEATURES)
		 
		print('*',tweet_text)

		#Go over it char by char
		for character, features in zip(tweet_text,features):
			
			#Find best matching trigram at this point
			scores_per_instance = []

			for instance in instances:
				score = sum([1 for a,b in zip(features,instance.features) if a==b])

				#Manually adding some more weight if the last words match
				if features[-1] == instance.features[-1]:
					score += 0.5 

				scores_per_instance.append((instance,score))

			scores_per_instance = sorted(scores_per_instance,key=lambda x: x[1],reverse=True)
			best_trigrams_for_tweet.append([(instance[0].features,instance[0].label) for instance in scores_per_instance[1:4]])

		result[twitter_user].append(best_trigrams_for_tweet)

open(OUTPUT_FILE,'w').write('var nearest_neighbors = '+dumps(result)+';')