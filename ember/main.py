
"""`main` is the top level module for your Flask application."""

# Import the Flask Framework

import appengine_config
from google.appengine.api import memcache
from flask import Flask, send_from_directory, redirect, request
from google.appengine.ext import ndb
import json
from datetime import datetime as dt
import os
import traceback

from tweetutils import Tweetbit, process_tweetfile_ndb, parse_list_of_tweetbits
from tweetutils import text_parse

app = Flask(__name__)
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.


class Start(ndb.Model):
    isInitialized = ndb.StringProperty()
    
@app.before_first_request
def init():
    rlist = []
    parentKey = ndb.Key("State", "loaded")
    rlist=Start.query().fetch(1)
    if len(rlist)>0:
        print "Datastore initialized: Skipping data load"
        pass
    elif len(rlist)==0:
        print "Seeding Google datastore"
        result = seed_datastore()
        if result=="DONE":
            start = Start(parent=parentKey, isInitialized="true")
            start.put()
            print "data store complete - putting start object"
        else:
            print "Exception encountered: No Start entity created"
    return
        
@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return redirect("/static/index.html")

@app.route('/insert')
def insert():
    try:
        term = "test"
        #pkey = ndb.Key("Term", term,"Tweetbit", term + dt.now().isoformat() )
        #tweet = Tweetbit(parent = pkey, latitude=10, longitude=222.003, timestamp=dt.now().isoformat())
        #tweet.put()
        parentkey = ndb.Key("Term",term)
        out = Tweetbit.query(ancestor=parentkey).fetch(20)
    except Exception as e:
        out= None
        e.message
    return parse_list_of_tweetbits(out)
    #return "200 A OK"

@app.route("/search")
def search():
    message = ""
    term = request.args['term']
    term = text_parse(term)[0]
    print term, ' loaded'
    response_data = memcache.get(term)
    if response_data is not None:
        print "Found term in memcache"
        print response_data
        pass
    else:#Drafting query
        print "Not found in memcache, querying datastore"
        parentKey = ndb.Key("Term", term.strip())
        out = Tweetbit.query(ancestor=parentKey).fetch(1000)
        if len(out)>0:
            response_data = parse_list_of_tweetbits(out)
            memcache.add(key=term,value=response_data, time=3600)
    return response_data
    
def seed_datastore():
    pathToDump = os.path.join(os.getcwd(),"tweet_dump")
    message = "NOT DONE"
    for filename in os.listdir(pathToDump):
        filepath = os.path.join(pathToDump,filename)
        print "Processing", filename
        try:
            process_tweetfile_ndb(filepath)
            message = "DONE"
        except Exception as e:
            print e.message
            print traceback.print_exc()
    return message

@app.route('/sample')
def sample():
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
