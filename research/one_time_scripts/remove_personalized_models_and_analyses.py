from os import listdir, remove

ANALYSIS_FOLDER = '../analyses/'
MODELS_FOLDER = '../timbl_models/'

for filename in listdir(ANALYSIS_FOLDER):
	test_user, train_users = filename.split('.')

	if test_user in train_users.split('_'):
		print(filename)
		remove(ANALYSIS_FOLDER+filename)

for filename in listdir(MODELS_FOLDER):
	test_user, train_users, tweet_index, extension = filename.split('.')

	if test_user in train_users.split('_'):
		#print(filename)
		remove(MODELS_FOLDER+filename)