from .board import Board


class MemoryBoard(Board):

# The __init__ method is roughly what represents a constructor in Python.
    def __init__(self):
        Board.__init__(self)
        self._board = []

    def post_message(self, message):
        self._board.append(message)

# The use of lambda creates an anonymous function (which is callable). In the case of
# sorted the callable only takes one parameters.
# The syntax of lambda is the word lambda followed by the list of parameter names
# then a single block of code. The parameter list and code block are delineated by colon.
        self._board = sorted(self._board,
                             key=lambda a: a.timestamp, reverse=True)

    def get_message(self):
        if(len(self._board) > 0):
            return self._board.pop()
        else:
            return None
