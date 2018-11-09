import sys
import zmq
import threading
import random
import time
import signal
from time import sleep
from datetime import timedelta
from datetime import datetime


class Message(object):

	def __init__(self, type, sender, receiver, term, data):
		self.timestamp = str(datetime.now())[11:]

		self.type = type
		self.sender = sender
		self.receiver = receiver
		self.data = data
		self.term = term

	def Print(self, recvr):
		try:
			response = self.data["response"]
		except:
			response = None

		print "%-15s | %-4s | %-5s | %-4d | %-4d | %-2d\n" %(self.timestamp, self.type, response, self.sender, recvr, self.term),


class Client(object):

	def __init__(self):
		self.leader_port = 0
		self.x = 1
		self.port = 5556
		self.messageBoard = []
		self.currentterm = 0
		

	def start_client(self):
	        class Client_thread(threading.Thread):

			def run(thread):
					time.sleep(10)
					while True:
						time.sleep(10)
						context = zmq.Context()
						socket = context.socket(zmq.PUB)
						socket.bind("tcp://*:%d" % self.port)
						self.send_log()
		self.client_thread = Client_thread()
		self.client_thread.start()

	def post_message(self, message):
		
 
		
		if self.leader_port == 5551:
			server1.requests.append(message.data["entries"])
			server1.requestcount += 1
			server1.requestmsg = True
			print "%-15s : Message Sent from client to Server %s" % (str(datetime.now())[11:] , self.leader_port)

		elif self.leader_port == 5552:
			server2.requests.append(message.data["entries"])
			server2.requestcount += 1
			server2.requestmsg = True
			print "%-15s : Message Sent from client to Server %s" % (str(datetime.now())[11:] , self.leader_port)

		elif self.leader_port == 5553:
			server3.requests.append(message.data["entries"])
			server3.requestcount += 1
			server3.requestmsg = True
			print "%-15s : Message Sent from client to Server %s" % (str(datetime.now())[11:] , self.leader_port)

		elif self.leader_port == 5554:
			server4.requests.append(message.data["entries"])
			server4.requestcount += 1
			server4.requestmsg = True
			print "%-15s : Message Sent from client to Server %s" % (str(datetime.now())[11:] , self.leader_port)

		elif self.leader_port == 5555:
			server5.requests.append(message.data["entries"])
			server5.requestcount += 1
			server5.requestmsg = True
			print "%-15s : Message Sent from client to Server %s" % (str(datetime.now())[11:] , self.leader_port)	

	

	def send_log(self):
		log_message = Message(
			"AE",
			self.port,
			self.leader_port,
			self.currentterm,
			{
				"clientId": self.port,
				"entries": self.x
			})
		self.x = self.x + 1
		self.post_message(log_message)


class Server(object):

	def __init__(self, port, state):
		self.state = state
		self.port = port
		self.messageBoard = []
		self.currentTerm = 0
		self.restart_timer = True

		self.commitIndex = 0
		self.currentTerm = 0

		self.log = []
		self.logIndex = 0
		self.commits = []
		self.commitcount = {}
		self.requests = []
		self.requestmsg = False
		self.requestcount = -1

		self.lastLogIndex = 0
		self.lastLogTerm = None

		self.votes={}
		self.lastVote = None

		self.time_started = None
		self.timeout = None


	def post_message(self, message):
		self.messageBoard.append(message)

		

	def send_heartbeat(self):
		heartbeat = Message(
			"AE",
			self.port,
			None,
			self.currentTerm,
			{
				"leaderId": self.port,
				"prevLogIndex": self.lastLogIndex,
				"prevLogTerm": self.lastLogTerm,
				"entries": [],
				"leaderCommit": self.commitIndex
			})

		self.post_message(heartbeat)
	
	def send_log(self,Value,neighbors):
		self.neighbors = neighbors
		print "%-15s :  Logs Committed into the followers" % (str(datetime.now())[11:])
		log_entries = Message(
			"AE",
			self.port,
			None,
			self.currentTerm,
			{
				"leaderId": self.port,
				"prevLogIndex": self.lastLogIndex,
				"prevLogTerm": self.lastLogTerm,
				"entries": Value,
				"lastentry": self.log[self.logIndex-2],
				"lastLogIndex": self.logIndex-2,
				"leaderCommit": self.commitIndex
			})
		print "Logs"
		print "Leader"
		print "Server: %s , Log : %s " % (self.port,self.log)
		print "Followers" 
		for n in neighbors:
			n.logIndex += 1
			n.lastLogIndex += 1
			print "Server: %s , Log : %s " % (n.port,n.log)
		self.post_message(log_entries)

	def start_election(self):
		self.state = CANDIDATE
		self.currentTerm += 1
		client.currentterm = self.currentTerm
		self.lastVote = self.port

		RequestVote = Message(
			"RV",
			self.port,
			None,
			self.currentTerm,
			{
				"lastLogIndex": self.lastLogIndex,
				"lastLogTerm": self.lastLogTerm
			})

		self.post_message(RequestVote)

	def on_append_entries(self, message, neighbors):
		if message.term < self.currentTerm:
			self.send_append_entries_response(message, response = False)

		if message.data["entries"] == []:
			self.state = FOLLOWER
			self.restart_timer = True
		else:
			if message.data["lastLogIndex"] >= 0:
				if self.logIndex-2 == message.data["lastLogIndex"]:
					if self.log[self.logIndex-2] == message.data["lastentry"]:
						self.log.append(message.data["entries"])
					else:
						self.replicate_log(neighbors)
				else:
					self.replicate_log(neighbors)
			else:
				self.log.append(message.data["entries"])
				

			

	def send_append_entries_response(self, message, response = True):
		AppendEntriesResponse = Message(
			"AE-R",
			self.port,
			message.sender,
			self.currentTerm,
			{
				"response": response,
				"currentTerm": self.currentTerm
			})

		self.post_message(AppendEntriesResponse)

	def on_vote_request(self, message):

		if message.term < self.currentTerm:
			self.send_vote_response_message(message, response = False)
			return

		if self.lastVote is None:

			if message.data["lastLogTerm"] < self.lastLogTerm:
				self.lastVote = message.sender
				self.send_vote_response_message(message)

			elif message.data["lastLogTerm"] == self.lastLogTerm and message.data["lastLogIndex"] <= self.lastLogIndex :
				self.lastVote = message.sender
				self.send_vote_response_message(message)

			else:
				self.send_vote_response_message(message, response = False)
		else:
			self.send_vote_response_message(message, response = False)

	def send_vote_response_message(self, message, response = True):
		voteResponse = Message(
			"RV-R",
			self.port,
			message.sender,
			message.term,
			{
				"response": response
			})
		self.post_message(voteResponse)

	def on_vote_received(self, message):
		if message.sender not in self.votes and message.data["response"] == True:
			self.votes[message.sender] = message


			if len(self.votes.keys()) == 2:
				print "\n[%s: server %d became Leader]\n\n" % (str(datetime.now())[11:],self.port),
				client.leader_port = self.port
				self.state = LEADER
				self.restart_timer = True

	def on_append_entries_response(self, message):
		pass

	def log_append(self,message):
		self.log.append(message.data["entries"])
		print "Loh size : %d\n" % (len(self.log))

	def on_message(self, message, neighbors):

		if message.term > self.currentTerm:
			self.currentTerm = message.term
			self.state = FOLLOWER
			self.lastVote = None

		if message.type == "AE":
			self.on_append_entries(message, neighbors)
		elif message.type == "RV":
			self.on_vote_request(message)
		elif message.type == "RV-R":
			self.on_vote_received(message)
		elif message.type == "AE-R":
			self.on_append_entries_response(message)


	def onrequestreceived(self,index,neighbors):
		self.neighbors = neighbors
		self.send_log(self.log[index-1],self.neighbors)
		
	def replicate_log(self, neighbors):
		self.neighbors = neighbors
		for n in neighbors:
			nextIndex =  self.lastLogIndex if n.lastLogIndex > self.lastLogIndex else n.lastLogIndex
			while nextIndex > -1 and n.log[nextIndex] != self.log[nextIndex]:
				nextIndex -= 1
			nextIndex += 1
			n.log[nextIndex:]=[]
			print n.port
			i = nextIndex-1
			while i < self.lastLogIndex :
				i += 1
				n.log.append(self.log[i])


	def SetUpThreads(self, neighbors):
		self.neighbors = neighbors

		class SubscribeThread(threading.Thread):

			def run(thread):
				context = zmq.Context()
				socket = context.socket(zmq.SUB)
				for n in neighbors:
					socket.connect("tcp://localhost:%d" % n.port)
				socket.setsockopt(zmq.SUBSCRIBE, "")
				

				while True:
					if self.state == LEADER:
						if self.requestmsg== True:
							self.logIndex += 1
							self.log.append(self.requests[self.requestcount])
							print "%-15s : Requested committed onto the leader" % (str(datetime.now())[11:])
							print "Logs"
							print "Leader"
							print "Server: %s , Log : %s " % (self.port,self.log)
							print "Followers"
							for n in neighbors:
								print "Server: %s , Log : %s " % (n.port,n.log)
							self.requestmsg = False
							self.onrequestreceived(self.logIndex,self.neighbors)
					message = socket.recv_pyobj()
					if message.receiver == self.port or message.receiver is None:
						
						message.Print(self.port)
						self.on_message(message, neighbors)

			
		
			

		'''class PrintLog(threading.Thread):
			
			def run(thread):
				while True:
					time.sleep(3)
					print "Server: %s , Log : %s " % (self.port,self.log)'''


		class PublishThread(threading.Thread):

			def run(thread):

				context = zmq.Context()
				socket = context.socket(zmq.PUB)
				socket.bind("tcp://*:%d" % self.port)

				while True:
					if len(self.messageBoard)>0:
						message = self.messageBoard.pop(0)
						socket.send_pyobj(message)


		class StartTimer(threading.Thread):

			def run(thread):
				x = datetime.now()
				y = 0
				while True:
					while self.state != LEADER:
						self.time_started = time.time()
						self.timeout = random.randint(15,20)
						self.restart_timer = False

						while self.restart_timer == False and self.state != LEADER:
							if time.time() > self.time_started + self.timeout:
								print "\n[%s: server %d experienced timeout]\n\n" % (str(datetime.now())[11:],self.port),

								self.state = CANDIDATE
								self.votes = {}
								self.start_election()
								self.restart_timer = True
						if y == 10:
							print " Time Stamp : %s || Server Crashed %d " % (datetime.now(),self.port)
							e = threading.Event()
							e.wait(timeout=10)
						y=y+1
						
					while self.state == LEADER:
						if y == 10:
							print " Time Stamp : %s || Server Crashed %d inside function" % (datetime.now(),self.port)
							e = threading.Event()
							e.wait(timeout=10)
						y=y+1
						

		self.subscribeThread = SubscribeThread()
		self.publishThread = PublishThread()
		self.timeThread = StartTimer()

		self.subscribeThread.start()
		self.publishThread.start()
		self.timeThread.start()

signal.signal(signal.SIGINT, signal.SIG_DFL);

LEADER = 1
CANDIDATE = 2
FOLLOWER = 3

server1 = Server(5551, FOLLOWER)
server2 = Server(5552, FOLLOWER)
server3 = Server(5553, FOLLOWER)
server4 = Server(5554, FOLLOWER)
server5 = Server(5555, FOLLOWER)

servers = [server1, server2, server3, server4, server5]

client = Client()
client.start_client()



server1.SetUpThreads([server2, server3, server4, server5])
server2.SetUpThreads([server1, server3, server4, server5])
server3.SetUpThreads([server1, server2, server4, server5])
server4.SetUpThreads([server1, server2, server3, server5])
server5.SetUpThreads([server1, server2, server3, server4])

