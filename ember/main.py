
"""`main` is the top level module for your Flask application."""

# Import the Flask Framework
#import appengine_config

from flask import Flask, send_from_directory, redirect
from google.appengine.ext import ndb
import json
from datetime import datetime as dt

class Tweetbit(ndb.Model):
    latitude = ndb.FloatProperty()
    longitude = ndb.FloatProperty()
    timestamp = ndb.StringProperty()
    
app = Flask(__name__)
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return redirect("/static/index.html")

@app.route('/insert')
def insert():
    try:
        term = "test"
    #pkey = ndb.Key("Term", term,"Tweetbit", term + dt.now().isoformat() )
    #tweet = Tweetbit(parent = pkey, latitude=10, longitude=20.003, timestamp=dt.now().isoformat())
    #tweet.put()
        parentkey = ndb.Key("Term",term)
        out = Tweetbit.query(ancestor=parentkey).fetch(20)
    except Exception as e:
        out= e.message()
    return str(out)#"200 A OK"
    
@app.route('/search')
def search():
    output = {}
    output ["list"] = [(1,2),(50,100)]
    return json.dumps(output)

@app.route('/<path:filename>')
def send_static(filename):
    return send_from_directory('/static/', filename)
    
@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def page_not_found(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500
