import time
# class for the Base Message

class BaseMessage(object):
    AppendEntries = 0
    RequestVote = 1
    RequestVoteResponse = 2
    Response = 3

    def __init__(self, sender, receiver, term, data):
        self._timestamp = int(time.time())

        self._sender = sender
        self._receiver = receiver
        self._data = data
        self._term = term

    @property #Python @property is one of the built-in decorators. The main purpose of any decorator is to change your class methods or attributes in such a way so that the user of your class no need to make any change in their code
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
