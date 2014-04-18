import appengine_config
import json
import string
from google.appengine.ext import ndb
from datetime import datetime as dt

class Tweetbit(ndb.Model):
    term = ndb.StringProperty()
    latitude = ndb.FloatProperty()
    longitude = ndb.FloatProperty()
    timestamp = ndb.StringProperty()


def tweet_parse(tweet_json):
    tweet=json.loads(tweet_json.strip())
    output = []
    if tweet["geo"]!=None:
        timestamp= tweet["created_at"]
        coordinates = tweet["geo"]["coordinates"]
        words= text_parse(tweet["text"])
        output = make_tweetbits(coordinates,words,timestamp)
    return output

def tweet_put(tweet_json):
    tweet=json.loads(tweet_json.strip())
    output = 0
    if tweet["geo"]!=None:
        timestamp= tweet["created_at"]
        coordinates = tweet["geo"]["coordinates"]
        words= text_parse(tweet["text"])
        output = put_tweetbits(coordinates,words,timestamp)
        #print output
    return output

    
def make_tweetbits(geo,words,time):
    outlist = []
    for word in words:
        tweetkey = ndb.Key("Term", word,"Tweetbit", word + dt.now().isoformat() )
        #Fucked this up a little
        tweet = Tweetbit(parent = tweetkey, term=word, latitude=geo[0], longitude=geo[1], timestamp=time)
        outlist+=[tweet]
    return outlist

def put_tweetbits(geo,words,time):
    counter = 0
    for word in words:
        tweetkey = ndb.Key("Term", word,"Tweetbit", word + dt.now().isoformat() )
        #Fucked this up a little
        tweet = Tweetbit(parent = tweetkey, term=word, latitude=geo[0], longitude=geo[1], timestamp=time)
        tweet.put_async()
        counter+=1
    return counter

    
def compress_tweetfile(filepath):
    f = open(filepath,'r')
    outfilepath = filepath.rpartition('.')[0]+"_compressed.txt"
    o = open(outfilepath,'w')
    for line in f:
        tweet = json.loads(line)
        ctweet = {}
        ctweet["created_at"] = tweet["created_at"]
        ctweet["geo"] = tweet["geo"]
        ctweet["text"] = tweet["text"]
        o.write(json.dumps(ctweet)+'\n')
    o.close()
    f.close()
    print "File compressed"
    return
    
def process_tweetfile(filepath="cleanedtweets.txt"):
    f = open(filepath,'r')
    outlist = []
    for tweet_json in f:
        #print tweet_json
        outlist+= tweet_parse(tweet_json)
    print len(outlist)
    f.close()
    return

def process_tweetfile_ndb(filepath="cleanedtweets.txt"):
    print "Putting tweets into ndb"
    f = open(filepath,'r')
    tweetcounter = 0
    bitcounter = 0
    for tweet_json in f:
        #print tweet_json
        bitcounter+= tweet_put(tweet_json)
        tweetcounter+=1
    f.close()
    outstr = "Tweets: " + str(tweetcounter) + "\tTweetbits:" + str(bitcounter) +"\nDone"
    print "Processing complete"
    print outstr
    return outstr
    
def parse_list_of_tweetbits(listOfTweetBits):
    outlist = []
    for tweetbit in listOfTweetBits:
        outlist+=[(tweetbit.latitude,tweetbit.longitude)]
    jdict = {}
    jdict["list"]= outlist
    return json.dumps(jdict)

def text_parse(intext):
    intext = intext.lower()
    #Crunches text and returns a list of tokens
    text = ""
    for letter in intext:
        if letter in string.lowercase:
            text+=letter
        else:
            text+=" "
    return text.split()
    
