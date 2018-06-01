from os import listdir
from json import dumps

TWEET_FOLDER = 'tweets/'
OUTPUT_FOLDER = 'analyses/'

class Instance():

    def __init__(self,features,label):
        self.label = label
        self.features = features

    def __repr__(self):
        return str(self.features) + '->' + self.label

def tweet_to_instances(tweet,nr_of_features):

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
            instances.append(Instance(words[word_index:word_index+nr_of_features],label))
            word_index += 1

    return instances

if __name__ == '__main__':

    NR_OF_FEATURES = 3

    #Train
    analyzers = ['a','b']

    #Test
    for tweetfile in listdir(TWEET_FOLDER):
        twitter_user = tweetfile.replace('.txt','')

        for analyzer in analyzers:
            print('working on analyzer ',analyzer,' for ',twitter_user)

            result = open(OUTPUT_FOLDER+twitter_user+'.'+analyzer+'.txt','w')

            for tweet_index, tweet in enumerate(open(TWEET_FOLDER+tweetfile)):

                instances = tweet_to_instances(tweet,NR_OF_FEATURES)

                for character in tweet:
                    result.write(str(tweet_index)+'\t'+dumps({'best_pred_word':'ik','best_pred_char':'i'})+'\n')
