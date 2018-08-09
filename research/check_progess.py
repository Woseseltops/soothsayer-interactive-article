from os import listdir
from collections import Counter

EXPERIMENTS_FILE = 'experiment_instr.txt'
TWEETS_FOLDER = 'tweets/'
TIMBL_MODELS_FOLDER = 'timbl_models/'

tweets_done_per_experiment = Counter()

for line in open(EXPERIMENTS_FILE):
	test_user, train_users = line.strip().split()
	train_users = train_users.replace(',','_')

	tweets_done_per_experiment[test_user+'.'+train_users] = 0

for filename in listdir(TIMBL_MODELS_FOLDER):

	test_user, train_users, index, extension = filename.split('.')
	tweets_done_per_experiment[test_user+'.'+train_users] += 1

sorted_progress = sorted(tweets_done_per_experiment.items(),key=lambda x: x[1])

for experiment, tweets_done in sorted_progress:
	test_user,train_users = experiment.split('.')
	total_nr_of_tweets = len(open(TWEETS_FOLDER+test_user+'.txt').readlines())
	print(100*(tweets_done/total_nr_of_tweets),'%',experiment)