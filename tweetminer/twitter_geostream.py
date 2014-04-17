import oauth2 as oauth
import urllib2 as urllib
import json

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
  try:
    response = twitterreq(url, "GET", parameters)
    for line in response:
      line = line.strip()
      tweet = json.loads(line)
      if 'geo' in tweet:
        if tweet["geo"]!=None:
        #Only print tweets that have geo metadata
          print line
  except KeyboardInterrupt:
    pass
  except Exception as e:
    print e.message
    print "Restarting task- use KeyboardInterrupt to end"
    fetchsamples()
      

if __name__ == '__main__':
  fetchsamples()
  