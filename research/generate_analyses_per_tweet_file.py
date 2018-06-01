from os import listdir
from json import dumps

TWEET_FOLDER = 'tweets/'
OUTPUT_FOLDER = 'analyses/'

analyzers = ['a','b']

for tweetfile in listdir(TWEET_FOLDER):
    twitter_user = tweetfile.replace('.txt','')

    for analyzer in analyzers:
        print('working on analyzer ',analyzer,' for ',twitter_user)

        result = open(OUTPUT_FOLDER+twitter_user+'.'+analyzer+'.txt','w')

        for tweet_index, tweet in enumerate(open(TWEET_FOLDER+tweetfile)):
            for character in tweet:
                result.write(str(tweet_index)+'\t'+dumps({'best_pred_word':'ik','best_pred_char':'i'})+'\n')
