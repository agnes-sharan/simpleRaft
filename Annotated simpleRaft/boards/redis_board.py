# Redis is an open source key-value database
# Because Redis can accept keys in a wide range of formats, operations can be executed
# on the server and reduce the client's workload. Redis is often used for cache
# management and speeding up web applications.

import redis
from board import Board


class RedisBoard(Board):
    """This will create a message board that is backed by Redis."""
# The special syntax *args in function definitions in python is used to pass a variable number of arguments to a function. It is used to pass a non-keyworded, variable-length argument list.
# The special syntax **kwargs in function definitions in python is used to pass a keyworded, variable-length argument list.
    def __init__(self, *args, **kwargs):
        """Creates the Redis connection."""
        self.redis = redis.Redis(*args, **kwargs)

    def set_owner(self, owner):
        self.owner = owner

    def post_message(self, message):
        """This will append the message to the list."""
        pass

    def get_message(self):
        """This will pop a message off the list."""
        pass

    def _key(self):
        if not self.key:
            self.key = "%s-queue" % self.owner

        return self.key
