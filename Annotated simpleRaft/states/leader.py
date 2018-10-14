from collections import defaultdict
from .state import State
from ..messages.append_entries import AppendEntriesMessage


class Leader(State):

    def __init__(self):
        # defaultdict means that if a key is not found in the dictionary, then instead of a
        # KeyError being thrown, a new entry is created. The type of this new entry is given
        # by the argument of defaultdict.

        # for each server, index of the next log entry
        # to send to that server (initialized to leader
        # last log index + 1)
        self._nextIndexes = defaultdict(int)

        # for each server, index of highest log entry
        # known to be replicated on server
        # (initialized to 0, increases monotonically)
        self._matchIndex = defaultdict(int)

    def set_sever(self, server):
        self._sever = server
        self._send_heart_beat()

        for n in self._server._neighbors:
            # Initialise nextIndex and matchIndex
            self._nextIndexes[n._name] = self._server._lastLogIndex + 1
            self._matchIndex[n._name] = 0

    def on_response_received(self, message):
        # Was the last AppendEntries good?
        if(not message.data["response"]):
            # No, so lets back up the log for this node
            self._nextIndexes[message.sender] -= 1

            # Get the next log entry to send to the client.
            previousIndex = max(0, self._nextIndexes[message.sender] - 1)
            # Log entry at the previous index
            previous = self._server._log[previousIndex]
            # The current log entry to be sent
            current = self._server._log[self._nextIndexes[message.sender]]

            # Send the new log to the client and wait for it to respond.
            appendEntry = AppendEntriesMessage(
                self._server._name,
                message.sender,
                self._server._currentTerm,
                {
                    "leaderId": self._server._name,
                    "prevLogIndex": previousIndex,
                    "prevLogTerm": previous["term"],
                    "entries": [current],
                    "leaderCommit": self._server._commitIndex,
                })

            self._send_response_message(appendEntry)
        else:
            # The last append was good so increase their index.
            self._nextIndexes[message.sender] += 1

            # Are they caught up?
            if(self._nextIndexes[message.sender] > self._server._lastLogIndex):
                self._nextIndexes[message.sender] = self._server._lastLogIndex

            # The else part is missing here...

        return self, None

    def _send_heart_beat(self):
        # Message : sender, receiver, term, data
        # The receiver field will be filled by the send_message function
        # for each of the receivers in the system
        message = AppendEntriesMessage(
            self._server._name,
            None,
            self._server._currentTerm,
            {
                "leaderId": self._server._name,
                "prevLogIndex": self._server._lastLogIndex,
                "prevLogTerm": self._server._lastLogTerm,
                # "entries" is empty only for heartbeats
                "entries": [],
                "leaderCommit": self._server._commitIndex,
            })
        self._server.send_message(message)
