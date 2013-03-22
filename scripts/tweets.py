import xml.etree.ElementTree as ET
import cgi
import urllib2
import json

form=cgi.FieldStorage()
print "Content-type: application/json"
print

theLimit = int(form.getvalue("limit", None))

tweetXML = urllib2.urlopen('http://twitter.com/statuses/user_timeline/scubbo.xml')
theTree = ET.parse(tweetXML)

tweets = []

if theLimit == None or theLimit == '':
	tweetsDOM = theTree.findall('status')
	for tweet in tweetsDOM:
		tweets.append({'title': tweet.find('text').text, 'id': tweet.find('id').text, 'date': tweet.find('created_at').text})
else:
	tweetIterator = theTree.iterfind('status')
	while len(tweets) < theLimit:
		try:
			nextTweet = tweetIterator.next()
			tweets.append({'title': nextTweet.find('text').text, 'id': nextTweet.find('id').text, 'date': nextTweet.find('created_at').text})
		except StopIteration:
			break
print json.dumps(tweets)
