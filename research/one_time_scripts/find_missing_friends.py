from os import listdir

ANALYSIS_FOLDER = 'analyses/'
FRIENDS_FOLDER = 'references/'

models_per_user = {}

for filename in listdir(ANALYSIS_FOLDER):

	user, models = filename.split('.')

	if '_' in models:
		continue

	if user not in models_per_user.keys():
		models_per_user[user] = set()

	models_per_user[user].add(models)

for user, models in models_per_user.items():

	friends = [l.strip() for l in open(FRIENDS_FOLDER+user+'.txt')]
	
	for friend in friends:
		if friend not in models:
			print(user,friend)