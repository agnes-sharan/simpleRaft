import unittest

from ..boards.memory_board import MemoryBoard
from ..messages.append_entries import AppendEntriesMessage
from ..messages.request_vote import RequestVoteMessage
from ..servers.server import Server
from ..states.follower import Follower

class TestFollowerServer( unittest.TestCase ):

	# This sets up a system of two servers with the second having the first 
	# in its neighbour list.
	def setUp( self ):
		board = MemoryBoard()
		state = Follower()
		self.oserver = Server( 0, state, [], board, [] )

		board = MemoryBoard()
		state = Follower()
		self.server = Server( 1, state, [], board, [ self.oserver ] )

	# This checks for the invocation of on_message when a message is sent
	# from server0 -> server1
	def test_follower_server_on_message( self ):
		msg = AppendEntriesMessage( 0, 1, 2, {} )
		self.server.on_message( msg )

	# This is a test to ensure when the term of message is lesser than server term
	# the response field of the response message contains false indicating the same
	def test_follower_server_on_receive_message_with_lesser_term( self ):

		msg = AppendEntriesMessage( 0, 1, -1, {} )

		self.server.on_message( msg )

		self.assertEquals( False, self.oserver._messageBoard.get_message().data["response"] )

	# When the term of the server is behind that of the message, the term of the
	# server has to be pdated and that is checked in this function.
	def test_follower_server_on_receive_message_with_greater_term( self ):

		msg = AppendEntriesMessage( 0, 1, 2, {} )

		self.server.on_message( msg )

		self.assertEquals( 2, self.server._currentTerm )

	def test_follower_server_on_receive_message_where_log_does_not_have_prevLogTerm( self ):
		self.server._log.append( { "term": 100, "value": 2000 } )
		msg = AppendEntriesMessage( 0, 1, 2, { 
							"prevLogIndex": 0, 
							"prevLogTerm": 1, 
							"leaderCommit": 1, 
							"entries": [ { "term": 1, "value": 100 } ] } )

		self.server.on_message( msg )

		self.assertEquals( False, self.oserver._messageBoard.get_message().data["response"] )
		self.assertEquals( [], self.server._log )

	# This checks for the response on multiple values for the same term, and posting
	# a message in this case and invoking the appropriate action. 
	def test_follower_server_on_receive_message_where_log_contains_conflicting_entry_at_new_index( self ):

		self.server._log.append( { "term": 1, "value": 0 } )
		self.server._log.append( { "term": 1, "value": 200 } )
		self.server._log.append( { "term": 1, "value": 300 } )
		self.server._log.append( { "term": 2, "value": 400 } )

		msg = AppendEntriesMessage( 0, 1, 2, { 
							"prevLogIndex": 0, 
							"prevLogTerm": 1, 
							"leaderCommit": 1, 
							"entries": [ { "term": 1, "value": 100 } ] } )

		self.server.on_message( msg )
		self.assertEquals( { "term": 1, "value": 100 }, self.server._log[1] )
		self.assertEquals( [ { "term": 1, "value": 0 }, { "term": 1, "value": 100 } ], self.server._log )

	# This ensures proper updation of the log in the event of no previous log
	# existing in the server. 
	def test_follower_server_on_receive_message_where_log_is_empty_and_receives_its_first_value( self ):

		msg = AppendEntriesMessage( 0, 1, 2, { 
							"prevLogIndex": 0, 
							"prevLogTerm": 100, 
							"leaderCommit": 1, 
							"entries": [ { "term": 1, "value": 100 } ] } )

		self.server.on_message( msg )
		self.assertEquals( { "term": 1, "value": 100 }, self.server._log[0] )

	# This ensure the proper receipt of vote request message by ensuring that
	# the sender of the vote request message and the one logged as last vote 
	# are equal. 
	def test_follower_server_on_receive_vote_request_message( self ):
		msg = RequestVoteMessage( 0, 1, 2, { "lastLogIndex": 0, "lastLogTerm": 0, "entries": [] } )

		self.server.on_message( msg )

		self.assertEquals( 0, self.server._state._last_vote )
		self.assertEquals( True, self.oserver._messageBoard.get_message().data["response"] )

	
	def test_follower_server_on_receive_vote_request_after_sending_a_vote( self ):
		msg = RequestVoteMessage( 0, 1, 2, { "lastLogIndex": 0, "lastLogTerm": 0, "entries": [] } )

		self.server.on_message( msg )

		msg = RequestVoteMessage( 2, 1, 2, {} )
		self.server.on_message( msg )

		self.assertEquals( 0, self.server._state._last_vote )


