#n,u,y,s,e,a

class trip():
	def __init__(self,id,name):
		self.id = id
		self.name = name
		

def decode(fname="dests.txt"):
	places = []
	with open(fname,'r') as f:
		i = 0
		for line in f:
			parts = line.split('-')
			if parts[0] == '#n':

