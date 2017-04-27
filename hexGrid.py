import numpy as np

class GridObject(object):
	def __init__(self, pos, map):
		if not isinstance(pos, np.ndarray):
			self.pos = np.asarray(pos)
		else:
			self.pos = pos
		self.map = map
	def scale(self, to=1):
		pass

class Vertice(GridObject):
	def __init__(self, pos, map, rcpos):
		super(Vertice, self).__init__(pos, map)
		if not isinstance(pos, np.ndarray): self.rcpos = np.asarray(rcpos)
		else: self.rcpos = rcpos
		self.scaledRCpos = self.rcpos*1
	def __getitem__(self, key):
		return self.rcpos.__getitem__(key)
	def __iter__(self):
		return self.rcpos.__iter__()
	def scale(self, to=1):
		self.scaledRCpos = self.rcpos*to
	
class Edge(GridObject):
	def __init__(self, pos, map, points):
		super(Edge, self).__init__(pos, map)
		self.points = points
	def __getitem__(self, key):
		return self.points.__getitem__(key)
	def __iter__(self):
		return self.points.__iter__()

class Hex(GridObject):
	neighborDirections = np.asarray((
		(1, 0),
		(0, 1),
		(-1, 1),
		(-1, 0),
		(0, -1),
		(1, -1)
	))
	borderDirections = np.asarray((
		(0, 1, 0),
		(-1, 1, 1),
		(-1, 0, 2),
		(0, 0, 0),
		(0, 0, 1),
		(0, 0, 2)
	))
	cornerDirections = np.asarray((
		(0, 1, 0),
		(0, 0, 1),
		(-1, 1, 0),
		(0, -1, 1),
		(0, 0, 0),
		(1, -1, 1),
	))
	cornerRCDirections = np.linspace(1/6*np.pi, 11/6*np.pi, 6)
	centerMatrix = np.asarray((
		(np.sqrt(3), np.sqrt(3)/2),
		(0, 3/2)
	))
	# getAttrSwitch = {
		# 'x': self.getX,
		# 'y': self.getY,
		# 'z': self.getZ
	# }
	def __init__(self, pos, map):
		super(Hex, self).__init__(pos, map)
		posWithZero = np.asarray((self.pos[0], self.pos[1], 0))
		self.rcCenter = np.dot(self.centerMatrix, self.pos)
		self.neighborPositions = self.pos+self.neighborDirections
		self.borderPositions = posWithZero+self.borderDirections
		self.cornerPositions = posWithZero+self.cornerDirections
		self.cornerPositionPairs = np.empty(6)
		# for i in range(6):
			# (positions[i], positions[(i+1)%6])
	def __getitem__(self, key):
		return self.pos.__getitem__(key)
	def __iter__(self):
		return self.pos.__iter__()
	def __getattr__(self, attr):
		try:
			if attr=='x':
				return self.getX()
			elif attr=='y':
				return self.getY()
			elif attr=='z':
				return self.getZ()
		except KeyError:
			raise AttributeError(attr)
	def __repr__(self):
		return 'Hex'+self.pos.__str__()
	def getX(self):
		return self.pos[0]
	def getY(self):
		return self.pos[1]
	def getZ(self):
		return -self.pos[0]-self.pos[1]
	def getNeighbours(self):
		for pos in self.getNeighbourPositions():
			yield self.map.get(pos)
	def getBorders(self):
		for pos in self.getBorderPositions():
			yield self.map.getEdge(pos)
	def getCorners(self):
		for pos in self.cornerPositions:
			yield self.map.getCorner(pos)
	def getBorderCornerPairs(self):
		positions = self.cornerPositions
		for i in range(6):
			yield (positions[i], positions[(i+1)%6])
	def getRCCorners(self):
		for dir in self.cornerRCDirections:
			yield self.rcCenter+(np.cos(dir), np.sin(dir))
	
class HexMap(object):
	def __init__(self, hex = Hex):
		self.map = {}
		self.vertices = {}
		self.edges = {}
		self.drawableEdges = []
		self.hextype = hex
	def __iter__(self):
		return  self.map.__iter__()
	def __getitem__(self, slc):
		return self.getWithIterKey(self.map, slc)
	def __str__(self):
		return self.map.__str__()
	def __len__(self):
		return self.map.__len__()
	def getHex(self, pos, default = None):
		try: return self[pos]
		except KeyError: return default
	def getEdge(self, pos, default = None):
		try: return self.getWithIterKey(self.edges, pos)
		except KeyError: return default
	def getVertice(self, pos, default = None):
		try: return self.getWithIterKey(self.vertices, pos)
		except KeyError: return default
	def createHex(self, pos):
		self.map[pos] = hex = self.hextype(pos, self)
		for vert in zip((tuple(item) for item in hex.cornerPositions), hex.getRCCorners()):
			if vert[0] in self.vertices:
				continue
			self.vertices[vert[0]] = Vertice(vert[0], self, vert[1])
		for edge in zip((tuple(item) for item in hex.borderPositions), hex.getBorderCornerPairs()):
			if edge[0] in self.edges:
				continue
			self.edges[edge[0]] = Edge(edge[0], self, (self.getVertice(edge[1][0]), self.getVertice(edge[1][1])))
	def generateDrawableEdges(self, size):
		self.drawableEdges = [tuple(point.rcpos*size for point in self.edges[key]) for key in self.edges]
	def makeFromMovementRange(self, dist):
		for x, y in self.getMovementRangeCoord(dist): self.createHex((x, y))
	@staticmethod
	def getWithIterKey(frm, key):
		if isinstance(key, tuple): return frm[key]
		else: return frm[tuple(key)]
	@staticmethod
	def getMovementRangeCoord(dist):
		for x in range(-dist, dist+1):
			for y in range(max(-dist, -x-dist), min(dist, -x+dist)+1): yield x, y
		
def test():
	map = HexMap()
	map.makeFromMovementRange(1)
	print(len(map))
	print(len(map.vertices))
	print(len(map.edges))
	
if __name__=='__main__': test()