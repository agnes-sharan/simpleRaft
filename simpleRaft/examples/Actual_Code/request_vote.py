from .base import BaseMessage


class RequestVoteMessage(BaseMessage): #RequestVoteMessage inherits from Basemessage under base.py

    _type = BaseMessage.RequestVote

    def __init__(self, sender, receiver, term, data):
        BaseMessage.__init__(self, sender, receiver, term, data) #intialization


class RequestVoteResponseMessage(BaseMessage):

    _type = BaseMessage.RequestVoteResponse

    def __init__(self, sender, receiver, term, data):
        BaseMessage.__init__(self, sender, receiver, term, data) #inttialization
