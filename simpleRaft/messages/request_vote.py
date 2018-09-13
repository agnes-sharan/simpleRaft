from .base import BaseMessage


class RequestVoteMessage(BaseMessage):

	# Sets the type of Message in this case RequestVote = 1
    _type = BaseMessage.RequestVote

    # This initializes the BaseMessage with given parameters
    def __init__(self, sender, receiver, term, data):
        BaseMessage.__init__(self, sender, receiver, term, data)


class RequestVoteResponseMessage(BaseMessage):

	# Sets the type of Message in this case RequestVoteResponse = 2
    _type = BaseMessage.RequestVoteResponse

    # This initializes the BaseMessage with given parameters
    def __init__(self, sender, receiver, term, data):
        BaseMessage.__init__(self, sender, receiver, term, data)
