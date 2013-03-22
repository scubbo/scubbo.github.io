import cgi

print "Content-type: text/html"
print

form=cgi.FieldStorage()
theInput = form.getvalue("toDouble", 0)

print str(int(theInput)*2)
