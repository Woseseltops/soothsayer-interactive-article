from os import listdir
from collections import Counter

TWEETS_FOLDER = 'tweets/'

for filename in listdir(TWEETS_FOLDER):

    counter = Counter()

    for tweet in open(TWEETS_FOLDER+filename):
        for word in tweet.split():

            if word[0] == '@':
                counter[word[1:]] += 1

    print(filename,counter)