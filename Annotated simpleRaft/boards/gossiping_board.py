from .board import Board


class GossipingBoard(Board):
    """This will connect to the local gossiping daemon and post and
    get messages from that daemon.

    """

# In multitasking computer operating systems,
# a daemon is a computer program that runs as a background process, 
# rather than being under the direct control of an interactive user.
