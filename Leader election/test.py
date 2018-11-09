class Server(object):

	def __init__(self, port):
		self.port = port
		self.log = []
		self.logIndex = 0
		self.lastLogIndex = 0
	
	def neighbors_update(self, neighbors):
		self.neighbors = neighbors

	def replicate_log(self, neighbors):
		self.neighbors = neighbors
		for n in neighbors:
			nextIndex =  self.lastLogIndex if n.lastLogIndex > self.lastLogIndex else n.lastLogIndex
			while nextIndex > -1 and n.log[nextIndex] != self.log[nextIndex]:
				nextIndex -= 1
			nextIndex += 1
			n.log[nextIndex:]=[]
			print n.port
			i = nextIndex-1
			while i < self.lastLogIndex :
				i += 1
				n.log.append(self.log[i])

server1 = Server(5551)
server2 = Server(5552)
server3 = Server(5553)
server4 = Server(5554)
server5 = Server(5555)

server1.neighbors_update([server2, server3, server4, server5])
server2.neighbors_update([server1, server3, server4, server5])
server3.neighbors_update([server1, server2, server4, server5])
server4.neighbors_update([server1, server2, server3, server5])
server5.neighbors_update([server1, server2, server3, server4])

server1.log = [1,5,6,7,9]
server2.log = [2,3,4]
server3.log = [1,5,6,7,9,10]
server4.log = [1,5,7]
server5.log = [1,5,8]

server1.lastLogIndex = len(server1.log) - 1
server2.lastLogIndex = len(server2.log) - 1
server3.lastLogIndex = len(server3.log) - 1
server4.lastLogIndex = len(server4.log) - 1
server5.lastLogIndex = len(server5.log) - 1

print 'LOGS'
print(server1.log)
print(server2.log)
print(server3.log)
print(server4.log)
print(server5.log)

'''print(server1.lastLogIndex)
print(server2.lastLogIndex)
print(server3.lastLogIndex)
print(server4.lastLogIndex)
print(server5.lastLogIndex)'''

server1.replicate_log([server2, server3, server4, server5])

print 'LOGS'
print(server1.log)
print(server2.log)
print(server3.log)
print(server4.log)
print(server5.log)
