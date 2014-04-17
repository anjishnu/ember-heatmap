import json
import os

tweetsdir = os.path.join(os.getcwd(),'tweets')

def cleanfiles(tweetsdir=tweetsdir):
    for file in (os.listdir(tweetsdir)):
        file_clean(os.path.join(tweetsdir,file))
    return

def file_clean(filepath):
    try:
        f = open(filepath,'r')
        #cleanedfile = filepath.rpartition(".")[0] + 'cleaned.txt'
        cleanedfile = "cleanedtweets2.txt"
        fclean = open(cleanedfile,'a+')
        print "Creating file:", cleanedfile
        for line in f:
            tweet = json.loads(line)
            if 'place' in tweet:
                if tweet['place']!=None:
                    print "valid tweet found", tweet["place"]['country']
                    fclean.write(json.dumps(tweet)+'\n')
    except:
        f.close()
        fclean.close()
        print "Exiting gracefully, closing connections"
        
    print "Closing connections-"
    f.close()
    fclean.close()
    return

    
    