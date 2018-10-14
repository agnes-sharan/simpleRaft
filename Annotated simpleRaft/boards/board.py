# class MyClass(object): = new-style class
# class MyClass: = OLD-STYLE CLASS
# Used when defining base class objects


class Board(object):

# Python decided to do methods in a way that makes the instance to which the method
# belongs be passed automatically, but not received automatically: the first parameter
# of methods is the instance the method is called on.
    def set_owner(self, owner):
        self._owner = owner
        # The _ signals that these are private members.
        # It just means the those attributes are for internal use only
        # and if possible don't touch them.

    def post_message(self, message):
        """This will post a message to the board."""


    def get_message(self):
        """This will get the next message from the board.

        Boards act like queues, and allow multiple clients
        to write to them.
        """
