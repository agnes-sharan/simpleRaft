# Import Board class from file in same directory
# Boards are maintained to post and retreive messages like a queue
# Boards contain set_owner, post_message and get_message funtions
from .board import Board

# MemoryBoard class is derived from Board class
class MemoryBoard(Board):

    # This clears up the message board and sets it to null
    def __init__(self):
        Board.__init__(self)
        self._board = []

    # This will append the message sent as argument in the function call to 
    # the list dealing with the baord messages. Once the message is appended
    # it sorts the board in descending order of timestamp
    def post_message(self, message):
        self._board.append(message)

        self._board = sorted(self._board,
                             key=lambda a: a.timestamp, reverse=True)

    # This pops the last message on board list
    def get_message(self):
        if(len(self._board) > 0):
            return self._board.pop()
        else:
            return None
