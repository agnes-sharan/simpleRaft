import sys
import zmq
import threading
import random
import time
import signal
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

class Server(object):

	def __init__(self, port, state):
		self.state = state
		self.port = port
		self.messageBoard = []
		self.currentTerm = 0
		self.restart_timer = True

		self.commitIndex = 0
		self.currentTerm = 0

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

	def start_election(self):
		self.state = CANDIDATE
		self.currentTerm += 1
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

	def on_append_entries(self, message):
		if message.term < self.currentTerm:
			self.send_append_entries_response(message, response = False)

		if message.data["entries"] == []:
			self.state = FOLLOWER
			self.restart_timer = True

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

				self.state = LEADER
				self.restart_timer = True

	def on_append_entries_response(self, message):
		pass

	def on_message(self, message):

		if message.term > self.currentTerm:
			self.currentTerm = message.term
			self.state = FOLLOWER
			self.lastVote = None

		if message.type == "AE":
			self.on_append_entries(message)
		elif message.type == "RV":
			self.on_vote_request(message)
		elif message.type == "RV-R":
			self.on_vote_received(message)
		elif message.type == "AE-R":
			self.on_append_entries_response(message)

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
					message = socket.recv_pyobj()

					if message.receiver == self.port or message.receiver is None:
						message.Print(self.port)
						self.on_message(message)


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

				while True:
					while self.state != LEADER:
						self.time_started = time.time()
						self.timeout = random.randint(3,5)
						self.restart_timer = False

						while self.restart_timer == False and self.state != LEADER:
							if time.time() > self.time_started + self.timeout:
								print "\n[%s: server %d experienced timeout]\n\n" % (str(datetime.now())[11:],self.port),

								self.state = CANDIDATE
								self.votes = {}
								self.start_election()
								self.restart_timer = True

					while self.state == LEADER:
						time.sleep(0.1)
						self.send_heartbeat()

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


server1.SetUpThreads([server2, server3, server4, server5])
server2.SetUpThreads([server1, server3, server4, server5])
server3.SetUpThreads([server1, server2, server4, server5])
server4.SetUpThreads([server1, server2, server3, server5])
server5.SetUpThreads([server1, server2, server3, server4])
