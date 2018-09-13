
class Board(object): # function Board which inherits from object class 

    def set_owner(self, owner): # function, Rather than using special syntax (such as this) to refer to class instances from within methods, methods in Python must be defined with an explicit first parameter
        self._owner = owner # intialization of the owner or setting of the owner

    def post_message(self, message): #function
        """This will post a message to the board."""

    def get_message(self): #function
        """This will get the next message from the board.

        Boards act like queues, and allow multiple clients
        to write to them.
        """
