import zmq
import threading
import random


class Server(object):
	
	def __init__(self,name,state,neighbours):
		self._name = name
	        self._state = state
		self._neighbors = neighbors

	

class ZMQserver(Server):
	def __init__(self,name,state,neighbours,port=6666):
		super(ZeroMQServer, self).__init__(name, state, neighbors)
	        self._port = 6666	

	class StartTimer(threading.Thread):
	     def start(thread):
		rand = random.randint(150,301)
		while True:
		    timer.sleep(rand/100)   
		    # start election
		    break

	class SubscribeThread(threading.Thread):
            def run(thread):
                context = zmq.Context() 
                socket = context.socket(zmq.SUB)
                for n in neighbors:
                    socket.connect("tcp://%s:%d" % (n._name, n._port)) 
		
		self.timer = Timer()
		self.timer.daemon = True
     	        self.timer.start()
                while True: 
		    message = socket.recv()
     		    self.timer._stop()
                    #action on message
		    self.timer.daemon = True
		    self.timer.start()  	
                    
			
        class PublishThread(threading.Thread):
            def run(thread):
                context = zmq.Context()
                socket = context.socket(zmq.PUB)
                socket.bind("tcp://*:%d" % self._port)

                while True:
                    #send heartbeat
                    if not message:
                        continue 
                    socket.send(message)
 
        self.subscribeThread = SubscribeThread() 
        self.publishThread = PublishThread()
	

        self.subscribeThread.daemon = True
        self.subscribeThread.start()
        self.publishThread.daemon = True
        self.publishThread.start()
	
