import zmq
import threading
import random
import time
import signal

class Message(object):

    def __init__(self, type, sender, receiver, term, data):
        self.timestamp = int(time.time())

        self.type = type
        self.sender = sender
        self.receiver = receiver
        self.data = data
        self.term = term

class Server(object):

	def __init__(self, port, state):
		self.state = state
		self.port = port
		self.messageBoard = []

	def post_message(self, message):
        self.messageBoard.append(message)

	def on_message(self, message):
		if message.type == "AppendEntries":



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
					message = socket.recv()
					self.on_message(message)


		class PublishThread(threading.Thread):
			def run(thread):
				context = zmq.Context()
				socket = context.socket(zmq.PUB)
				socket.bind("tcp://*:%d" % self.port)

				while True:
				    if len(messageBoard)>0:
						message = messageBoard.pop(0)
						socket.send(message)


		class StartTimer(threading.Thread):
		     def run(thread):
				 while True:
					 time_started = time.time()
					 timeout = random.randint(3,5)

					 while restart_time == False:
						if time.time()>time_started + timeout:
							self.post_message("Start Election")

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
# server3 = Server(5553, FOLLOWER)
# server4 = Server(5554, FOLLOWER)
# server5 = Server(5555, FOLLOWER)


# server1.SetUpThreads([server2, server3, server4, server5])
# server2.SetUpThreads([server1, server3, server4, server5])
# server3.SetUpThreads([server1, server2, server4, server5])
# server4.SetUpThreads([server1, server2, server3, server5])
# server5.SetUpThreads([server1, server2, server3, server4])

server1.SetUpThreads([server2])
server2.SetUpThreads([server1])
