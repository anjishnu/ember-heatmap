import oauth2 as oauth
import urllib2 as urllib
import json
from time import time
import os
import requests

# See Assignment 1 instructions or README for how to get these credentials
access_token_key = "1420209648-1q9H7txbG9TF55isGWxSmjCtQ1pfX2pYoBAlrpa"
access_token_secret = "WiDW0FpqndoZrqoM39zHE8o6HJV8JuzOciIXC7Xbjk"

consumer_key = "ywEtQSq1TyxuZNoB8XGyNw"
consumer_secret = "kRw1jgBIK1LinMk9PUEKrpu2JJknASASRNM8OhiCO4"

_debug = 0

oauth_token    = oauth.Token(key=access_token_key, secret=access_token_secret)
oauth_consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)

signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

http_method = "GET"


http_handler  = urllib.HTTPHandler(debuglevel=_debug)
https_handler = urllib.HTTPSHandler(debuglevel=_debug)

'''
Construct, sign, and open a twitter request
using the hard-coded credentials above.
'''
def twitterreq(url, method, parameters):
  req = oauth.Request.from_consumer_and_token(oauth_consumer,
                                             token=oauth_token,
                                             http_method=http_method,
                                             http_url=url, 
                                             parameters=parameters)

  req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)

  headers = req.to_header()

  if http_method == "POST":
    encoded_post_data = req.to_postdata()
  else:
    encoded_post_data = None
    url = req.to_url()

  opener = urllib.OpenerDirector()
  opener.add_handler(http_handler)
  opener.add_handler(https_handler)

  response = opener.open(url, encoded_post_data)

  return response

def fetchsamples():
  url = "https://stream.twitter.com/1/statuses/sample.json"
  parameters = []
  counter = 0
  try:
    response = twitterreq(url, "GET", parameters)
    for line in response:
      line = line.strip()
      tweet = json.loads(line)
      if 'geo' in tweet:
        if tweet["geo"]!=None:
        #Only print tweets that have geo metadata
          counter+=1
          print line
  except KeyboardInterrupt:
    pass
  except Exception as e:
    print e.message
    print "Restarting task- use KeyboardInterrupt to end"
    counter+=fetchsamples()
    return counter
  return counter

def compress_tweet(tweet):
    ctweet = {}
    ctweet["created_at"] = tweet["created_at"]
    ctweet["geo"] = tweet["geo"]
    ctweet["text"] = tweet["text"]
    return ctweet

def modfetchsamples(f, tstart):
  url = "https://stream.twitter.com/1/statuses/sample.json"
  parameters = []
  counter = 0
  try:
    response = twitterreq(url, "GET", parameters)
    for line in response:
      if time()-tstart>TIME_LIMIT:
        return counter
      line = line.strip()
      tweet = json.loads(line)
      if 'geo' in tweet:
        if tweet["geo"]!=None:
        #Only print tweets that have geo metadata
          counter+=1
          f.write(line+'\n')
          #print line
  except KeyboardInterrupt:
    pass
  except Exception as e:
    print e.message
    print "Restarting task- use KeyboardInterrupt to end"
    return counter
  return counter

# This constant defines how long the tweet_mining
# will run for. //Download Data for 10 minutes 
TIME_LIMIT=600
output_file = os.path.join(os.getcwd(),"minedtweets",
                           "current_tweets.txt")

# Getting rid of recursion
def main():
  tstart = time()
  writefile = open(output_file,'w')
  counter =0 
  while(time()-tstart<TIME_LIMIT):
    counter+=modfetchsamples(writefile, tstart)
    print "Time elapsed", time()-tstart
  writefile.close()
  print "Ending mining operation"
  print "Total time", time()-tstart
  print counter, "valid tweets found"
  print "Beginning JSON Parsing"
  readfile = open(output_file,'r')
  array = read_file(readfile)
  print "array loaded of length", len(array)
  readfile.close()
  print "sending json request"
  r = json_post_data(array)
  print "Posting complete with response :"
  print r
  print "Deleting temp file"
  os.remove(output_file)
  print "File deleted"
  return


LIMIT = 1000 #Limiting JSON Request to 1000 tweets
def read_file(readfile):
  arr = []
  counter=0
  for line in readfile:
    if counter<1000:
      tweet = json.loads(line.strip())
      ctweet = compress_tweet(tweet)
      arr+=[ctweet]
      counter+=1
  return arr

def json_post_data(array):
  #url = "http://localhost:8080/add_tweets"
  url = "http://ember-heatmap.appspot.com/add_tweets"
  headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
  print json.dumps(array)
  r = requests.post(url, data=json.dumps(array), headers=headers)
  print r
  return r
                     

if __name__ == '__main__':
  #fetchsamples()
  main()
