import urllib2
import cgi

form=cgi.FieldStorage()
parent_word = form.getvalue("parentWord", "entertainment")

print "Content-type: text/html"
print

llen=len(parent_word)

def index_inc(index_list):
     for index in range(len(index_list)):
          if index_list[-(index+1)]<llen-index-1:
               index_list[-(index+1)]+=1
               for i in range(index):
                    index_list[-(index-i)] = index_list[-(index+1)]+i+1
               break
     return index_list

def generate_word(index_list):
  ###Given a list of indices, returns the corresponding sub-word
  return reduce(lambda x, y: x+y, [parent_word[i] for i in index_list])

def find_words(length):
  ###This finds all sub-words of the parent word
  word_list=[]
  index_list=[]
  for i in range(length):
    index_list.append(i)
  while index_list[0] != llen - len(index_list):
    word_list.append(generate_word(index_list))
    index_list = index_inc(index_list)
  return word_list
  
###Now do stuff

words=urllib2.urlopen('http://www.puzzlers.org/pub/wordlists/enable1.txt').readlines()
words=[word[:-1] for word in words]

word_list=[]
for length in range(llen):
  word_list+=find_words(length+1)

genuine_word_list=[]

for word_number in range(len(word_list)):
  if word_list[word_number] in words and word_list[word_number] not in genuine_word_list:
    genuine_word_list.append(word_list[word_number])
if parent_word in words:
  genuine_word_list.append(parent_word)

print str(len(genuine_word_list))+':'
for word in genuine_word_list:
  print word+':'
