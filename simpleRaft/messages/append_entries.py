from .base import BaseMessage # '.' is basically a relative import for packages from the same directory


class AppendEntriesMessage(BaseMessage): #inherits BaseMessage class under base.py

    _type = BaseMessage.AppendEntries

    def __init__(self, sender, receiver, term, data):
        BaseMessage.__init__(self, sender, receiver, term, data) # intializes the object with the timestamp, sender, reciver, thhe current term,and also the data
