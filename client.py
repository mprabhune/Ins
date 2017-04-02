##Title : Client server instant messaging
##Program ID: client.py
##Programming lang: Python 3.5
##Date : 03-09-2017
##Student Name : Mukund Prabhune
##Student ID : 1001231716

###import packages
import socket
import threading
from time import sleep
import signal
import sys

#create socket 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#connect socket to local IP on port 8080
s.connect(('127.0.0.1', 8080))
#get username from console. This is individual usernames for each client run
u = input('Username: ')
#socket communication takes byte code format. incoming string is converted to byte #format
s.send(str.encode(u + '>reg>'+'null'))
#ask user to connect
v = input('do you want to connect y/n?')
#if yes, ask user, username to whom he wants to connect.
#if n, register user on server
if v == 'y':
	v = input('who do you want to connect to?')
	s.send(str.encode(u + '>conn>'+v))

###encode byte format string and send it to socket
def se(s):
    while 1:
        s.send(str.encode(u + '>show>' + input()))
        sleep(0.05)
###receive byte format string from socket, maximum 1024 characters packet size.
def re(s):
    while 1:
        r = s.recv(1024)
        if r != 'No messages':
            print (r)
        sleep(0.05)

###Define sending and receving thread objects. These threads separates 
###two client communications. Hence two set of two clients can communicate 
###with each other without interferance of other pair of client
thse = threading.Thread(target = se , args = (s,))
thse.daemon = False
thse.start()
thre = threading.Thread(target = re , args = (s,))
thre.daemon = False
thre.start()

###this signal handler function close the socket  for cntl+C keyboard interrupt
def signal_handler(signal, frame):
        print('You pressed Ctrl+C to shuntdown')
#        thse.exit()
#        thre.exit()
        s.close()
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

###seek server for every second for communication
while 1:
    sleep(1)
    pass
	
