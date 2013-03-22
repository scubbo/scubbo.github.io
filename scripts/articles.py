import xml.etree.ElementTree as ET
import cgi

form=cgi.FieldStorage()
print "Content-type: text/html"
print

theLimit = form.getvalue("limit", None)
theFields = form.getvalue("fields", None)

theTree = ET.parse('../nftnfrss.xml')

articles = []

if theLimit = None:
	articlesDOM = theTree.findall('channel/item')
	for article in articlesDOM:
		articles.append({'title': article.find('title').text, 'description': article.find('description').text, 'link': article.find('link').text})
else:
	articleIterator = theTree.iterfind('channel/item')
	while len(articles) < theLimit:
		try:
			nextArticle = articleIterator.next()
			articles.append({'title': nextArticle.find('title').text, 'description': nextArticle.find('description').text, 'link': nextArticle.find('link').text})
		except StopIteration:
			break
