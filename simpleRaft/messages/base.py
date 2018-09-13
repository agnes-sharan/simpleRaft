import time


class BaseMessage(object):
    AppendEntries = 0
    RequestVote = 1
    RequestVoteResponse = 2
    Response = 3

    # This keeps track of when the message was received, what term 
    # it was received in, the data and the two communication endpoints
    def __init__(self, sender, receiver, term, data):
        self._timestamp = int(time.time())

        self._sender = sender
        self._receiver = receiver
        self._data = data
        self._term = term

    # The following functions are just function calls that allow access
    # to specific attributes in the BaseMessage class object
    @property
    def receiver(self):
        return self._receiver

    @property
    def sender(self):
        return self._sender

    @property
    def data(self):
        return self._data

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def term(self):
        return self._term

    @property
    def type(self):
        return self._type
