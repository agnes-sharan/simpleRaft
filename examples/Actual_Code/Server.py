import zmq
import threading
import random

class Server(object):

	def __init__(self, port, state):
		self.port = name
	    self.state = state
        self.port = port

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
					# self.on_message(message)
					print message

		class PublishThread(threading.Thread):
		    def run(thread):
		        context = zmq.Context()
		        socket = context.socket(zmq.PUB)
		        socket.bind("tcp://*:%d" % self.port)

		        while True:
		            # if not message:
		            #     continue
		            # socket.send(message)
				    to_client = random.randrange(1,215) - 80
				    print "%s:%d" %(self.port,to_client)
				    socket.send("%s:%d" %(self.port,to_client))
				    time.sleep (1)

	    self.subscribeThread = SubscribeThread()
	    self.publishThread = PublishThread()


	    self.subscribeThread.daemon = True
	    self.subscribeThread.start()

	    self.publishThread.daemon = True
	    self.publishThread.start()

	def Communicate(peer):



LEADER = 1
CANDIDATE = 2
FOLLOWER = 3

server1 = Server(5551, FOLLOWER)
server2 = Server(5552, FOLLOWER)
server3 = Server(5553, FOLLOWER)

server1.SetUpThreads([server2, server3])
server2.SetUpThreads([server1, server3])
server3.SetUpThreads([server1, server2])
