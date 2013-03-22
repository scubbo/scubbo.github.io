#!/usr/bin/python
import twitter, random, threading
import imaplib, smtplib, socket
from email.Parser import Parser
import datetime, time, email, email.Utils
import re, sys
import atexit
import pickle

'''Format of a lyric (which cannot be it's own class if it is to be pickled)
(text, song, artist, added_on, added_by, used) - all strings'''

class twitterBot:
  def __init__(self, active=True, immediate_post=False):

    #sys.stderr = file('errorlog'+ str(time.time()) + '.txt', 'w')
    self.api = twitter.Api(consumer_key='GOtXT1w70K8MEzYRvkvg', consumer_secret='nCgAfdsDegqDE2yUyasiZ5Hh0JEUVHifGvjzvVj1DSU', access_token_key='472324117-sunUrJ0ArCXa9gmdQGdQMbJ1jAzkeVsHUcYCl0wU', access_token_secret='aXZ332LJNsrYEjWooTz4pbocdb2vxCIq9zX1WCLM')
    self.lastposted=0
    self.logfile=file('logs.txt', 'r+')
    self.logfile.write(str(datetime.datetime.now()) + '\tInitialisation\n')
    self.update()
    if active:
      s=threading.Thread(None, self.post_thread, args=[immediate_post])
      s.daemon=True
      print 'Starting post thread'
      s.start()
      time.sleep(60)
      t=threading.Thread(None, self.listen_thread)
      t.daemon=True
      print 'Starting listen Thread'
      t.start()

  def update(self):
    '''grabs program variables from source files'''
    with file('lyrics.pkl', 'rb') as f:
      while True:
        try:
          self.lyrics=pickle.load(f)
        except EOFError:
          break
    self.total=len(self.lyrics)
    self.used = [i for i in range(self.total) if self.lyrics[i]['used'] == 'true']
    if len(self.used)>=self.total:
      for lyric in self.lyrics:
        lyric['used'] = 'false'
      self.used=[]
    f=file('last.txt', 'r+')
    lines=f.readlines()
    if len(lines) > 0:
      self.lastMention=long(lines[0])
    else:
      self.lastMention=long(-1)
    f.close()
  
  def post(self, tweet_number):
    try:
      self.api.PostUpdate(self.lyrics[tweet_number]['text'] + ' PLEASE RT')
      #print lyrics[tweet_number]
      self.lyrics[tweet_number]['used'] = 'true'
      with file('lyrics.pkl', 'rb') as f:
        while True:
            try:
                spoof = pickle.load(f)
            except EOFError:
                break
      with file('lyrics.pkl', 'wb') as f:
        pickle.dump(self.lyrics, f)
      self.logfile.write(str(datetime.datetime.now()) + '\tPosting\n')
      self.lastposted=time.time()
    except:
      self.logfile.write(str(datetime.datetime.now()) + '\tSomething went wrong with posting, retrying\n')
      self.post(tweet_number)
    
  def addlyric(self, lyric):
    if type(lyric)==type('') and len(lyric) <= 130:
      self.lyrics.append({'text':lyric, 'used':'false'})
      with file('lyrics.pkl', 'rb') as f:
        while True:
            try:
                spoof = pickle.load(f)
            except EOFError:
                break
      with file('lyrics.pkl', 'wb') as f:
        pickle.dump(self.lyrics, f)
      self.update()
    else:
      raise ValueError('Tweet is too long!' + repr(len(lyric)))
  
  def random_post(self):
    textToUse = random.choice([i for i in range(self.total) if i not in self.used])
    self.post(textToUse)
    return textToUse
  
  def replyToMentions(self):
#    try:
    print 'lastMention is '+str(self.lastMention)
    if self.lastMention==-1:
        mentions = self.api.GetMentions(lastMention)
        self.lastMention=self.api.GetPublicTimeline()[-1].id
    else:
        mentions = self.api.GetMentions(self.lastMention)
    if len(mentions)>0:
        self.lastMention = mentions[-1].id
    else:
        lastMention = self.api.GetPublicTimeline()[-1].id
    file('last.txt', 'w').write(str(self.lastMention))
    if len(mentions) == 0:
        print 'No mentions to reply to'
    for tweet in mentions:
        print 'Replying to user: '+str(tweet.user.screen_name)+' who tweeted "' + str(tweet.text)+'"'
        self.reply(tweet.user.screen_name)
#    except:
#      self.logfile.write(str(datetime.datetime.now())+'\tSomething went wrong replying to mentions\n')
      
  def reply(self, recip):
    l=self.lyrics[random.choice([i for i in range(self.total) if not self.lyrics[i]['used'] == 'true'])]['text']
    if len(l) < 138 - len(recip):
      try:
        self.api.PostUpdate('@' + recip + ' ' + l)
        print 'Replied with "'+str(l)+'"'
      except twitter.TwitterError:
        self.reply(recip)
    else:
      self.reply(recip)
  
  
  def monitorEmail(self):
    server = imaplib.IMAP4_SSL("imap.gmail.com")
    server.login("trexlyrics", "Haiguyswhatsup")
    r=server.select("INBOX")
    
    r, data = server.search(None, "(UNSEEN SUBJECT 'addlyric')")
    
    if len(data[0]) > 0:
      print 'There are '+str(len(data[0]))+' e-mails'
      p = Parser()
      
      lyriclist=[]
      patt1=re.compile('lyric:[.\s]*:end')
      patt2=re.compile('<.*>')
      for num in data[0].split():
        r, data = server.fetch(num, "(RFC822.TEXT body[header.fields (from)])")
        text=data[0][1].replace('=\r\n', '').replace('\r\n', '').replace('=85', '...')
        if text.find('Content-Type: text/html')!=-1: text = text[:text.find('Content-Type: text/html')]
        print 'Chomping on '+text+' from '+str(num)
        fromaddr=data[1][1]
        while True:
          if text.find('lyric:')!=-1 and text.find(':end')!=-1:
            lyriclist.append((text[text.find('lyric:'):text.find(':end')][6:], re.findall(patt2, fromaddr)[0][1:-1]))
            text = text[text.find(':end')+4:]
          else:
            break
      else: print 'Inbox searched, '+str(len(lyriclist))+' prospective lyrics found.'
      smtpserver=smtplib.SMTP("smtp.gmail.com", 587)
      smtpserver.ehlo()
      smtpserver.starttls()
      smtpserver.ehlo()
      smtpserver.login('trexlyrics@gmail.com', 'Haiguyswhatsup')
      #smtpserver.sendmail('trexlyrics@gmail.com', 'scubbojj@gmail.com', 'To: scubbojj@gmail.com\r\nFrom: trexlyrics@gmail.com\r\nSubject: debug - listening\r\nDebug email. I am listening.')
      for l in lyriclist:
        if len(l[0])>1:
          try:
            self.addlyric(l[0])
            print 'Just added lyric: "'+l[0]+'" from '+l[1]
            self.logfile.write(str(datetime.datetime.now())+'\tJust added lyric: "'+l[0]+'" from '+l[1]+'\n')
            smtpserver.sendmail('trexlyrics@gmail.com', l[1], 'To: '+l[1]+'\r\nFrom: trexlyrics@gmail.com\r\nSubject: Lyric accepted\r\n\r\nThank you, your lyric "'+l[0]+'" has been accepted to the T-rex lyrics project.  See it in action at www.twitter.com/trexlyrics !')
          except ValueError:
            smtpserver.sendmail('trexlyrics@gmail.com', l[1], 'To: '+l[1]+'\r\nFrom: trexlyrics@gmail.com\r\nSubject: Too long!\r\nSorry, your lyric "'+l[0]+'" was too long ('+str(len(l[0]))+' characters).  Maybe try again?')
            print 'Error on lyric submitted by '+l[1]+' - Too long ("'+l[0]+'", '+str(len(l[0]))+' characters)'
            self.logfile.write(str(datetime.datetime.now())+'\tError on lyric submitted by '+l[1]+' - Too long ("'+l[0]+'", '+str(len(l[0]))+' characters)\n')
        else:
          print 'That\'s too short'
      else: print 'All done!'
      smtpserver.close()
    else: print 'No prospective lyrics in the inbox'
        
  def listen(self):
#    try:
    self.replyToMentions()
    self.monitorEmail()
      #self.logfile.write(str(datetime.datetime.now()) + '\tListening\n')
#    except:
#      self.logfile.write(str(datetime.datetime.now())+'\tSomething went wrong listening\n')
#      self.listen()
  
  #Looping code below sets up a listening server that responds to data received
  #with either a reply/addlyric, or a post
  """print 'Starting listen server'
  while True:
    HOST = ''                 # Symbolic name meaning all available interfaces
    PORT = 50007              # Arbitrary non-privileged port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()
    time=datetime.datetime.now()
    print '\nConnected from ',  addr, ' at ' + str(time.hour) + ':' + str(time.minute) + ':' + str(time.second)
    while 1:
        data = conn.recv(1024)
        if not data: break
        if data == '1':
          num = go()
          response = 'Lyric posted: '+lyrics[num] 
        elif data[:6]=='lyric:':
          try:
            addlyric(data[6:data.find(':end')])
            response = 'Lyric added: "'+data[6:data.find(':end')]+'"' 
          except ValueError:
            response = 'Error adding lyric: "'+data[6:data.find(':end')]+'" - too long ('+str(data.find(':end')-6)+' characters).'
        else:
          response =  'Listening...'
        print response
        conn.send(response)
        if response[-12:] == 'Listening...': listen() #This break with the pattern is justified in that listening takes a while, leading to delay on response for client.
    conn.close() """
  
  
  #Threading code
  def listen_thread(self):
    sys.stderr.flush()
    while True:
      self.listen()
      time.sleep(120)
      
  def post_thread(self, urgent=False):
    while True:
      if not urgent:
        if time.time()-self.lastposted > 61 and time.localtime()[3]%8==2 and time.localtime()[4]==0:
          print 'Posting then sleeping now!'
          self.random_post()
          time.sleep(28700)
      else:
        print 'You are rushing!'
        self.random_post()
        urgent=False
