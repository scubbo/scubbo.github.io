import socket
import sys
import time

HOST = 'localhost'        # The remote host
PORT = 50007              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
if len(sys.argv)>0:
  i = sys.argv[1]
  if i in ['help', 'h']:
    print 'Enter \'1\' to post a lyric.\nEnter \'lyric:<lyrics here>:end\' to submit a lyric.\nEnter any other string to perform a listen (monitor email submissions and reply to @ mentions.)'
  elif i in ['quit', 'q']:
    pass
  else:
    s.send(i)
    data = s.recv(1024)
    print repr(data)
  s.close()
else:
  s.send('1')
  data = s.recv(1024)
  print data
