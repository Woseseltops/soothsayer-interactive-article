from os import listdir
from itertools import chain
from collections import Counter
from json import dumps

from timbl import TimblClassifier

TWEET_FOLDER = 'tweets/'
OUTPUT_FOLDER = 'analyses/'

class Instance():

	def __init__(self,features,label,author,original_tweet_index):
		self.label = label
		self.features = features
		self.author = author
		self.original_tweet_index = original_tweet_index

	def __repr__(self):
		return '{' + str(self.features) + '->' + self.label + '}'

def tweet_to_instances(tweet,nr_of_features,author,original_tweet_index):

	NOTHING_INDICATOR = '_ '

	instances = []

	enclosed_text = nr_of_features*NOTHING_INDICATOR+tweet+nr_of_features*NOTHING_INDICATOR
	words = enclosed_text.split()
	word_index = 0

	while True:
		label = words[word_index+nr_of_features]

		if label == '_':
			break
		else:
			instance = Instance(words[word_index:word_index+nr_of_features],label,author,original_tweet_index)

			instances.append(instance)
			word_index += 1

	return instances

def get_instances_for_twitter_user(username):

	#Collect all tweets and instances we have for this user
	total_tweets = []
	total_instances = []

	for tweet_index, tweet in enumerate(open(TWEET_FOLDER+username+'.txt')):
		total_tweets.append(tweet)
		instances_for_this_tweet = tweet_to_instances(tweet,NR_OF_FEATURES,tweet_index,username)
		total_instances += instances_for_this_tweet

	return total_instances

def find_matching_model_files(training_file_folder,test_user,train_users):

	for filename in listdir(training_file_folder):
		
		test_u,train_u,tweet_index,extension = filename.split('.')
		if test_u == test_user and train_u.split('_') == train_users:
			return True

	return False

def pick_best_matching_words_from_dictionary(distribution,target,n):

	matches = []
	ordered_distribution = sorted(distribution.items(),key=lambda x: x[1])

	for word, freq in ordered_distribution:

		if len(word) >= len(target) and word[:len(target)] == target:
			matches.append(word)

		if len(matches) == n:
			break

	return matches

if __name__ == '__main__':

	INSTRUCTION_FILE = 'experiment_instr.txt'
	TIMBL_MODELS_FOLDER = 'timbl_models/'
	NR_OF_FEATURES = 3
	REMEMBER_NR_OF_OPTIONS = 3

	#Go trhough the file with instructions
	for line in open(INSTRUCTION_FILE):

		#Parse the isntruction
		line.strip()
		test_user, train_users = line.split()
		train_users = train_users.split(',')

		#Is this instructions already in progress? Go to the next one
		if find_matching_model_files(TIMBL_MODELS_FOLDER,test_user,train_users):
			continue

		#Create train instances for this experiment
		train_instances = list(chain([get_instances_for_twitter_user(train_user) for train_user in train_users]))[0]

		#Go through the tweets of the test user
		for tweet_index, tweet in enumerate(open(TWEET_FOLDER+test_user+'.txt')):

			#Train the model on all tweets except this one
			timbl_model_name = test_user+'.'+'_'.join(train_users)+'.'+str(tweet_index)
			classifier = TimblClassifier(TIMBL_MODELS_FOLDER+timbl_model_name,'-a 0 -k 1 +vs')
			word_frequencies = Counter()

			for instance in train_instances:
				if instance.author == test_user and instance.original_tweet_index == tweet_index:
					continue

				classifier.append( instance.features, instance.label)
				word_frequencies[instance.label]+= 1

			classifier.train()

			#Here the prediction starts
			tweet_so_far = ''
			current_word = ''

			for character in tweet:

				#Administration about the tweet so far
				tweet_so_far += character
				current_word += character
				words_so_far = tweet_so_far.split()

				if character != ' ':
					words_so_far = words_so_far[:-1]
				else:
					current_word = ''

				#Prepare the the info for a classifier predction
				features = words_so_far[-NR_OF_FEATURES:]

				while len(features) < NR_OF_FEATURES:
					features = ['_'] + features

				#Do the classifier prediction
				classlabel, distribution, distance = classifier.classify(features)
				best_matching_words_from_context = pick_best_matching_words_from_dictionary(distribution,current_word,REMEMBER_NR_OF_OPTIONS)

				#Extend info with regular frequency list material
				if len(best_matching_words_from_context) < REMEMBER_NR_OF_OPTIONS:
					best_matching_words_from_freqlist = pick_best_matching_words_from_dictionary(word_frequencies,current_word,REMEMBER_NR_OF_OPTIONS-len(best_matching_words_from_context))
				else:
					best_matching_words_from_freqlist = []

				print(tweet_so_far,'|',best_matching_words_from_context,best_matching_words_from_freqlist)

			#result = open(OUTPUT_FOLDER+twitter_user+'.'+analyzer+'.txt','w')
		break

#Nog toevoegen: nearest neighbours ook opslaan?