from .board import Board # importing package from same directory


class GossipingBoard(Board): #GossipingBoard inherits from Board
    """This will connect to the local gossiping daemon and post and
    get messages from that daemon.

    """
