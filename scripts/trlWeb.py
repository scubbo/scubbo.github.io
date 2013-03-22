import cgi

form=cgi.FieldStorage()
role = form.getvalue("role")

if role == 'getLyrics':
    print "Content-type: text/html"
    print
    
    print '<ul class="lyricsList">'
    import pickle
    with file('Twitterbot/lyrics.pkl', 'rb') as f:
        while True:
            try:
                theLyrics = pickle.load(f)
            except EOFError:
                break
    with file('Twitterbot/lyrics.pkl', 'wb') as f:
        pickle.dump(theLyrics, f)
    for lyric in theLyrics:
        print '<li>'+lyric['text']+'</li>'
    print '</ul>'
elif role == 'getJSON':
    print "Content-type: application/json"
    print 
    
    import pickle
    with file('Twitterbot/lyrics.pkl', 'rb') as f:
        while True:
            try:
                theLyrics = pickle.load(f)
            except EOFError:
                break
    with file('Twitterbot/lyrics.pkl', 'wb') as f:
        pickle.dump(theLyrics, f)
    import json
    print json.dumps(theLyrics)
elif role == 'setJSON':
    print "Content-type: text/plain"
    print
    
    import pickle, json
    theJSON = form.getvalue("theJSON")
    theLyrics = json.loads(theJSON)
    with file('Twitterbot/lyrics.pkl', 'rb') as f:
        while True:
            try:
                spoof = pickle.load(f)
            except EOFError:
                break
    with file('Twitterbot/lyrics.pkl', 'wb') as f:
        pickle.dump(theLyrics, f)
    
    print "Thank you! We got " + str(len(theLyrics)) + " things"
elif role == 'test':
    print 'This is test data'
