from os import listdir
from collections import Counter
from sys import argv

TWEETS_FOLDER = 'tweets/'
REFERENCES_FOLDER = 'references/'
MINIMUM_AMOUNT_OF_REFERENCES = 10
OUTPUT = False

def clean_user_name(name):
	return name.replace("'s",'').replace('?','').replace('!','').replace(':','').replace('”','')

try:
	users = [user.lower().strip() for user in open(argv[1])]
except FileNotFoundError:
	users = [argv[1]]

total_references = set()
references_per_user = dict()

for user in users:

	references_per_user[user] = set()
	counter = Counter()

	for tweet in open(TWEETS_FOLDER+user+'.txt'):
	    for word in tweet.split():

	        if word[0] == '@':
	            counter[word[1:]] += 1

	for ref,freq in counter.items():
		
		ref = clean_user_name(ref)

		if len(ref) > 0 and freq > MINIMUM_AMOUNT_OF_REFERENCES and ref not in users:
			total_references.add(ref)
			references_per_user[user].add(ref)

	if OUTPUT:
		open(REFERENCES_FOLDER+user+'.txt','w').write('\n'.join(references_per_user[user]))

for user, freq in counter.most_common():

	if len(user) > 0 and freq > MINIMUM_AMOUNT_OF_REFERENCES:
		print(freq,user)