from .base import BaseMessage

# This inherits class BaseMessage from base.py
class AppendEntriesMessage(BaseMessage):

	# Sets the type of Message in this case AppendEntries = 0
    _type = BaseMessage.AppendEntries

    # This initializes the BaseMessage with given parameters
    def __init__(self, sender, receiver, term, data):
        BaseMessage.__init__(self, sender, receiver, term, data)
