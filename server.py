##Title : Client server instant messaging
##Program ID: server.py
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
import string

###Global thread variables (objects)
thtx = ""	#thread object for sending message
thrx = ""	#thread object for recieving message

#command explanation for socket, bind and listen
#define socket object
#bind socket object to local IP on port 8080
#start server in listen state. It takes maximum 10 connections in queue

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1', 8080))
s.listen(10)
c = {} 		#define global dictionary to collect incoming username and messages

###Initiate sending thread. This function takes connection and username as arguments.
###it parse the client message with '>' delimiter into dictionary and delete the ###username
###this thread waits for 5 ms using sleep command,to get the response from client.
 
def clientthreadTx(conn, user_name):
	while 1:
		if len(c[user_name]) > 1:
			conn.send(str.encode(c[user_name][0] + '>' + c[user_name][1]))
			del c[user_name][1]
		sleep(0.05)
	conn.close()

###Initiate receving thread. This function takes connection as arguments.	
def clientthreadRx(conn):				
	while 1:
		data = conn.recv(1024)
		#if data == 0:
		#connection down notify peer c[user_name][0]			
		#incoming data is in bytes format, hence decode it back to string
		data = data.decode("utf-8")
		#parse incoming data with '>' to get user_name, protocol(action) and message	
		e = data.split('>')				

		print(e)
		sleep(0.05)						#waits for 5ms to get the data from client
		##if incoming data formate is not in "<user_name>action>message", pring error
		if len(e) != 3:
			print("Message format Error")			
			pass
			
		cmd = e[1]
		##register new user to the server.This is first attribute of incoming data
		if cmd == 'reg':
			#registration
			user_name = e[0]
			c[user_name] = [""]
			### to register new user, initiate sending thread
			thtx = threading.Thread(target = clientthreadTx, args = (conn, user_name))
			thtx.daemon = False
			thtx.start()
		##establish connection with the already register user, which is stored in ##dictionary object	
		elif cmd == 'conn':
			#make connection
			user_name = e[0]
			#check connection
			c[user_name][0] = e[2]
			c[e[2]][0] = [""]
			c[e[2]][0] = user_name
		##show incoming communication between two users on the server 	
		elif cmd == 'show':
			user_name = e[0]
			c[c[user_name][0]].append(e[2])
		else:
			print("unknown command " + cmd)
		sleep(0.05)
	conn.close()	##close connection once communication is over

###this 
def signal_handler(signal, frame):
		print('You pressed Ctrl+C to shuntdown')
#		thrx.exit()
#		thtx.exit()
		s.close()		
		sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

###main function to accept the incoming socket request. Intiate receving thread	
while 1:
	conn, addr = s.accept() 
	thrx = threading.Thread(target = clientthreadRx, args = (conn,))
	thrx.daemon = False
	thrx.start()

	sleep(0.05)
s.close()
