import unittest

from ..boards.memory_board import MemoryBoard
from ..messages.base import BaseMessage

class TestMemoryBoard( unittest.TestCase ):

	# This initialises the memory baord by setting an empty list for baord
	def setUp( self ):
		self.board = MemoryBoard()

	# This checks for the functioning of post_message() function by posting a 
	# message then popping it off to see whether the messages match
	def test_memoryboard_post_message( self ):

		msg = BaseMessage( 0, 0, 0, 0 )	
		self.board.post_message( msg )
		self.assertEquals( msg, self.board.get_message() )

	# This is a test to ensure message posting is sorted in the order of decreasing
	# timestamp as defined in post_message()
	def test_memoryboard_post_message_make_sure_they_are_ordered( self ):

		msg = BaseMessage( 0, 0, 0, 0 )
		msg2 = BaseMessage( 0, 0, 0, 0 )
		msg2._timestamp -= 100
	
		self.board.post_message( msg )
		self.board.post_message( msg2 )

		self.assertEquals( msg2, self.board.get_message() )

