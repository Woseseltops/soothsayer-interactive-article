from sys import argv
from twython import Twython, TwythonError

class Tweet():

    def __init__(self,id,author,content):
        self.id = id
        self.author = author
        self.content = content
        self.automatic_classifications = {}

    def package(self):

        return '\t'.join([str(getattr(self,propertyname)) for propertyname in PACKAGE_ORDER])

def create_twitter_connection(passwordfile):

    app_key, app_secret, oauth_token, oauth_token_secret = open(passwordfile).read().split()
    return Twython(app_key, app_secret, oauth_token, oauth_token_secret)

def collect_tweets_for_user(user, passwordfile, exclude_retweets=False):
    twitter_connection = create_twitter_connection(passwordfile)
    no_tweets_received = False
    all_tweets = []
    page = 1

    while not no_tweets_received:

        try:
            new_raw_tweets = twitter_connection.get_user_timeline(screen_name=user, 
                                                            count=200, page=page, 
                                                            exclude_replies=False,
                                                            tweet_mode='extended')
        except TwythonError:
            print('Twython is sad :(')
            break

        if len(new_raw_tweets) < 1:
            no_tweets_received = True
        else:

            for raw_tweet in new_raw_tweets:
                current_tweet = Tweet(raw_tweet['id'], raw_tweet['user']['screen_name'],
                                      clean_tweet_text(raw_tweet['full_text']))
                try:
                    raw_tweet['retweeted_status']
                except:
                    all_tweets.append(current_tweet)

        page += 1

    return all_tweets

def clean_tweet_text(tweet_text):
    tweet_text = tweet_text.encode('utf8')
    result = str(tweet_text).strip().replace('\n',' | ')

    return result

if __name__ == '__main__':

    #mine_everything_for_twitter_users.py [input_list_file] [password_file]

    OUTPUT_FOLDER = 'tweets/'

    for twitter_user in open(argv[1]):
        twitter_user = twitter_user.strip()

        print('downloading tweets for ',twitter_user)

        #save every tweet found to a seperate line
        open(OUTPUT_FOLDER+twitter_user+'.txt','w').write('\n'.join([tweet.content for tweet in collect_tweets_for_user(twitter_user.strip(),argv[2],exclude_retweets=True)]))