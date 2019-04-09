import requests
from bs4 import BeautifulSoup
try:
    import cPickle as pickle
except:
    import pickle
import os
import sys
import time

def getStatus( key ):
    if( key == 'A' ):
        return 'American'
    elif( key == 'I' ):
        return 'International, w/o US Degree'
    elif( key == 'U' ):
        return 'International, w US degree'
    else:
        return 'Unkown'

def getUpdates( resList, prevTopRes ):
    idx = 0
    for res in resList:
        if ( res == prevTopRes ):
            idx = resList.index( res )
            return resList[:idx]
    return resList

def notifyUpdates( updates, url ):
    updateFile = open("updates.txt","w")
    if( sys.platform.startswith('linux') ):
        #Linux system. Install notify2 --  "sudo pip install notify2"
        import notify2
        if not notify2.init("Basics"):
            print "Couldn't init notify2 module"
        else:
            n = notify.Notification("Gradcafe Watcher", "You have some updates regarding admits/rejects to universities from gradcafe")
            if not n.show():
                print "Failed to show notification"
    elif( sys.platform.startswith('darwin') ):
        #Mac OSX. Install pync -- "sudo pip install pync"
        import pync
        try:
            pync.Notifier.notify("You have some updates regarding admits/rejects to universities from gradcafe. Click to open site", \
            title="Gradcafe Watcher", open=url)
        except:
            print "Notifications didn't work out"
    elif( sys.platform.startswith('Windows') ):
        #Lel, you must be insane to think I have support for Windows
        pass

    for update in updates:
        #Sorry for the ugly format :(
        str = "College : {} | Program : {} | Decision : {} | Status : {} | Date : {} | Comments : {} ".format(
            update['College'], update['Program'], update['Decision'], update['Status'], update['Date'], update['Comments']
        )
        str += "\n"
        updateFile.write( str )
    updateFile.close()

def getResults( url, collegeList ):
    headers = {
            #Robot trying to be a human. This is AI! :P
           'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
    }
    text = requests.get(url, headers=headers).text
    soup = BeautifulSoup( text, "html.parser" )
    results = [ ]
    results += soup.findAll( attrs={'class':'row0'} )
    results += soup.findAll( attrs={'class':'row1'} )
    resList= [ ]
    for res in results:
        resDict = { }
        tdElements = res.findAll( 'td' )
        college = tdElements[0].get_text()
        #This block looks so cool
        for coll in collegeList:
            #People are stupid. Need to account for randomness
            if ( college in coll ) or ( coll in college ):
                break
        else:
            continue
        resDict['College'] = college
        resDict['Program'] = tdElements[1].get_text().encode('ascii', 'ignore')
        resDict['Decision'] = tdElements[2].get_text().encode('ascii', 'ignore')
        resDict['Status'] = getStatus( tdElements[3].get_text() ).encode('ascii', 'ignore')
        resDict['Date'] = tdElements[4].get_text().encode('ascii', 'ignore')
        resDict['Comments'] = tdElements[5].get_text().encode('ascii', 'ignore')
        resList.append( resDict )
    
    if( os.path.exists('results.p') ):
        prevTopRes = pickle.load( open( 'results.p', 'rb' ) )[0]
    else:
        prevTopRes = None
    updates = getUpdates( resList, prevTopRes )
    if len(updates) is not 0:
        notifyUpdates( updates, url )
    else:
        #No updates
        pass
    return resList
    
if __name__ == '__main__':
    ''' Provide your stream (search string)'''
    stream = "computer science"
    
    ''' Provide the list of colleges you want to watch for. Ensure to keep the list exhaustive'''
    collegeList = [ "CMU", "Carnegie Mellon University", "UCSD", "UC San Diego", "University of California San Diego" ]

    ''' Proivde a time interval to refresh within'''
    interval = 30 * 60 #30 minutes

    stream = stream.replace(" ","+")
    url = "http://thegradcafe.com/survey/index.php?q={}".format( stream )
    while( True ):
        resList = getResults( url, collegeList )
        pickle.dump( resList, open( 'results.p','wb' ) )
        time.sleep( interval )
    