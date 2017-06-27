import tweepy
import MySQLdb

#pip install tweepy
#pip install mysqlclient

consumer_key    = 'c1WsPZTfqedj5ChMKZaFvrkWk'
consumer_secret = 'A1LZGPwkyHo7WwmPdC7jfmfyWVOfJXalpXly8GohAuexUD011Y'
access_token    = '3593453541-gu5plnoVovPTLtYfYZx8WzavDYbCci0xLK0lw42'
access_token_secret = 'EUpEZoFiWKrDNUxRpIxOT3q7h5V7qEjpH1ai5Yr6p7KyC'


auth = tweepy.OAuthHandler(consumer_key=consumer_key, consumer_secret=consumer_secret)
auth.set_access_token(access_token, access_token_secret)

#api = tweepy.API(auth)
api = tweepy.API(auth, wait_on_rate_limit_notify=True, wait_on_rate_limit=True)


# Create query string for public tweets from country 'Guatemala'
places = api.geo_search(query="GUATEMALA", granularity="country")
place_id = places[0].id
 
q="place:%s" % place_id 


import unicodedata

def strip_accents(text):

    try:
        text = unicode(text, 'utf-8')
    except NameError: # unicode is a default on python 3 
        pass
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text)


#import regex
import re
from unidecode import unidecode

#start process_tweet
def processTweet(tweet):
    # process the tweets

    #Convert to lower case
    tweet = tweet.lower()
    #Convert www.* or https?://* to URL
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',tweet)
    #Convert @username to AT_USER
    tweet = re.sub('@[^\s]+','AT_USER',tweet)
    #Remove additional white spaces
    tweet = re.sub('[\s]+', ' ', tweet)
    #Replace #word with word
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    #trim
    tweet = tweet.strip('\'"')
    #accented characters
    tweet = unidecode(tweet)
    #remove special characters
    tweet = re.sub('[^A-Za-z0-9]+', ' ', tweet)
    tweet = strip_accents(tweet)
    #remove emoticons
    myre = re.compile(u'['
                      u'\U0001F300-\U0001F64F'
                      u'\U0001F680-\U0001F6FF'
                      u'\u2600-\u26FF\u2700-\u27BF]+', re.UNICODE)
    #tweet = myre.sub('', tweet)
    #tweet = unidecode(tweet)
    #tweet = tweet.encode("ascii")
    return str(tweet)


db = MySQLdb.connect("localhost","root","terranostra","tesis" )
cursor = db.cursor()
public_tweets = api.search(q=q, lang="es", rpp=1000, since_id="2017-01-01")#, until="2017-01-03")

for tweet in public_tweets:
    #print(tweet.id)
    #print(tweet.text)
    #print(tweet.created_at)
    tweet_id = tweet.id
    text = processTweet(tweet.text)
    date = tweet.created_at
    print(text)
    try:
        cursor.execute( 'insert into tweets(id, text, date) values("%d","%s", "%s")' % (tweet_id, text, date) )
    except:
        pass
    db.commit()
db.close()