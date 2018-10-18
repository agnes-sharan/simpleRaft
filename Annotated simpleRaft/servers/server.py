import zmq
import threading

class Server(object):

    def __init__(self, name, state, log, messageBoard, neighbors):
        # A number like 0,1, ...
        self._name = name
        self._state = state
        # An array of dicts of the form {"term":  , "value":   }
        self._log = log
        # An object which is an array
        self._messageBoard = messageBoard
        # An array of server objects
        self._neighbors = neighbors
        self._total_nodes = 0

        # Index of highest log entry known to be committed
        self._commitIndex = 0
        self._currentTerm = 0
        # Index of highest log entry applied to state machine
        self._lastApplied = 0

        self._lastLogIndex = 0
        self._lastLogTerm = None

        self._state.set_server(self)
        # If state is Leader - Starts sending haeartbeats
        self._messageBoard.set_owner(self)

    def send_message(self, message):
        for n in self._neighbors:
            message._receiver = n._name
            n.post_message(message)

    def send_message_response(self, message):
        # Send response to a single receiver
        n = [n for n in self._neighbors if n._name == message.receiver]
        if(len(n) > 0):
            n[0].post_message(message)

    def post_message(self, message):
        self._messageBoard.post_message(message)

    def on_message(self, message):
        # The return value of any on_message function is the state and response
        # of the server. Change of state can happen depending upon the messages received
        # E.g: Follower -> Leader upon receiving a valid AppendEntries RPC
        state, response = self._state.on_message(message)

        self._state = state


class ZeroMQServer(Server):
    def __init__(self, name, state, log, messageBoard, neighbors, port=6666):
        super(ZeroMQServer, self).__init__(name, state, log, messageBoard, neighbors)
        self._port = 6666

# Define a new subclass of the Thread class.
        class SubscribeThread(threading.Thread):
            # override the run(self [,args]) method to implement what the thread
            # should do when started.
            def run(thread):
                context = zmq.Context()
                socket = context.socket(zmq.SUB)
                for n in neighbors:
                    socket.connect("tcp://%s:%d" % (n._name, n._port))

                while True:
                    message = socket.recv()
                    self.on_message(message)

        class PublishThread(threading.Thread):
            def run(thread):
                context = zmq.Context()
                socket = context.socket(zmq.PUB)
                socket.bind("tcp://*:%d" % self._port)

                while True:
                    message = self._messageBoard.get_message()
                    if not message:
                        continue # sleep wait?
                    socket.send(message)

# Create an instance of the threads
        self.subscribeThread = SubscribeThread()
        self.publishThread = PublishThread()

# Some threads do background tasks, like sending keepalive packets, or performing
# periodic garbage collection, or whatever. These are only useful when the main
# program is running, and it's okay to kill them off once the other, non-daemon,
# threads have exited.
# By setting them as daemon threads, you can let them run and forget about them,
# and when your program quits, any daemon threads are killed automatically.
        self.subscribeThread.daemon = True

# Once you have created the new Thread instance then start
# a new thread by invoking the start(), which in turn calls run() method.
        self.subscribeThread.start()
        self.publishThread.daemon = True
        self.publishThread.start()
