from .state import State

from ..messages.request_vote import RequestVoteResponseMessage


class Voter(State):
    # Class Voter is inherited from class State

    def __init__(self):
        # A class constructor
        # Variables declared inside this as instance-level variables
        self._last_vote = None

    def on_vote_request(self, message):
        if(self._last_vote is None and
           message.data["lastLogIndex"] >= self._server._lastLogIndex):
            self._last_vote = message.sender
            self._send_vote_response_message(message)
        else:
            self._send_vote_response_message(message, yes=False)
            # The first argument is the object which invoked the function

        return self, None

    def _send_vote_response_message(self, msg, yes=True):
        voteResponse = RequestVoteResponseMessage(
            self._server._name,
            msg.sender,
            msg.term,
            {"response": yes})
        self._server.send_message_response(voteResponse)