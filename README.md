ember-heatmap
=============

A heapmap for twitter with a GUI built on top of Google App Engine : ember-heatmap.appspot.com

Built by Anjishnu Kumar for COMS 6998: Cloud Computing and Big Data


Right now there is not a lot of data on the server because of the Google App Engine's API call limitations. 
Code isn't stable enough for production launch yet. Tweetminer is designed to be run on a vanilla Linux box - download tweets from Twitter's Streaming API and insert them into the datastore via HTTP calls. 

- To do:
- Convert tweetminer uploads into a bulkloader session call.
