import redis # importing packages, importing everything
# Redis is an open source (BSD licensed), in-memory data structure store, used as a database, cache and message broker. It supports data structures such as strings, hashes, lists, sets, sorted sets with range queries, bitmaps, hyperloglogs and geospatial indexes with radius queries. Redis has built-in replication, Lua scripting, LRU eviction, transactions and different levels of on-disk persistence, and provides high availability via Redis Sentinel and automatic partitioning with Redis Cluster

from board import Board # importing Board from board where board is the folder and Board is the class

class RedisBoard(Board): # class, RedisBoard inherits from Board
    """This will create a message board that is backed by Redis."""

    def __init__(self, *args, **kwargs):# *args in function definitions in python is used to pass a variable number of arguments to a function, **kwargs in function definitions in python is used to pass a keyworded, variable-length argument list
        """Creates the Redis connection."""
        self.redis = redis.Redis(*args, **kwargs) # self is a replacement for 'this' keyword from c++

    def set_owner(self, owner):
        self.owner = owner

    def post_message(self, message):
        """This will append the message to the list."""
        pass # pass" keyword (a statement) to indicate that nothing happens

    def get_message(self):
        """This will pop a message off the list."""
        pass

    def _key(self):
        if not self.key:
            self.key = "%s-queue" % self.owner # saving owner-queue as a string

        return self.key
