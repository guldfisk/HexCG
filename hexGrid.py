import numpy as np

class GridObject(object):
	def __init__(self, pos, map):
		if not isinstance(pos, np.ndarray): self.pos = np.asarray(pos)
		else: self.pos = pos
		self.map = map

class Vertice(GridObject):
	def __init__(self, pos, map, rpos):
		super(Vertice, self).__init__(pos, map)
		if not isinstance(pos, np.ndarray): self.rpos = np.asarray(rpos)
		else: self.rpos = rpos
	def __getitem__(self, key):
		return self.rpos.__getitem__(key)
	def __iter__(self):
		return self.rpos.__iter__()
	
class Edge(GridObject):
	def __init__(self, pos, map, points):
		super(Edge, self).__init__(pos, map)
		self.points = points
	def __getitem__(self, key):
		return self.points.__getitem__(key)
	def __iter__(self):
		return self.points.__iter__()

class Hex(GridObject):
	neighborDirections = (
		np.asarray((1, 0)),
		np.asarray((0, 1)),
		np.asarray((-1, 1)),
		np.asarray((-1, 0)),
		np.asarray((0, -1)),
		np.asarray((1, -1))
	)
	borderDirections = (
		np.asarray((0, 1, 0)),
		np.asarray((-1, 1, 1)),
		np.asarray((-1, 0, 2)),
		np.asarray((0, 0, 0)),
		np.asarray((0, 0, 1)),
		np.asarray((0, 0, 2))
	)
	cornerDirections = (
		np.asarray((0, 1, 0)),
		np.asarray((0, 0, 1)),
		np.asarray((-1, 1, 0)),
		np.asarray((0, -1, 1)),
		np.asarray((0, 0, 0)),
		np.asarray((1, -1, 1)),
	)
	cornerRCDirections = np.linspace(1/6*np.pi, 11/6*np.pi, 6)
	centerMatrix = np.asarray((
		(np.sqrt(3), np.sqrt(3)/2),
		(0, 3/2)
	))
	def __init__(self, pos, map):
		super(Hex, self).__init__(pos, map)
		self.posWithZero = np.asarray((self.pos[0], self.pos[1], 0))
	def __getattr__(self, attr):
		if attr=='x': return self.pos[0]
		if attr=='y': return self.pos[1]
		if attr=='z': return -self.pos[0]-sels.pos[1]
		raise AttributeError(attr)
	def __repr__(self):
		return 'Hex'+self.pos.__str__()
	def getNeighbourPositions(self):
		for dir in self.neighborDirections: yield self.pos+dir
	def getNeighbours(self):
		for pos in self.getNeighbourPositions(): yield self.map.get(pos, None)
	def getBorderPositions(self):
		for dir in self.borderDirections: yield self.posWithZero+dir
	def getBorders(self):
		for pos in self.getBorderPositions(): yield self.map.getEdge(pos, None)
	def getBorderCornerPairs(self):
		positions = tuple(self.getCornerPositions())
		for i in range(6): yield (positions[i], positions[(i+1)%6])
	def getCornerPositions(self):
		for dir in self.cornerDirections: yield self.posWithZero+dir
	def getCorners(self):
		for pos in self.getCornerPositions(): yield self.map.getCorner(pos, None)
	def getRCCenter(self):
		return np.dot(self.centerMatrix, self.pos)
	def getRCCorners(self):
		c = self.getRCCenter()
		for dir in self.cornerRCDirections: yield c+(np.cos(dir), np.sin(dir))
	
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
		hex = self.hextype(pos, self)
		self.map[pos] = hex
		for vert in zip((tuple(item) for item in hex.getCornerPositions()), hex.getRCCorners()):
			if vert[0] in self.vertices: continue
			self.vertices[vert[0]] = Vertice(vert[0], self, vert[1])
		for edge in zip((tuple(item) for item in hex.getBorderPositions()), hex.getBorderCornerPairs()):
			if edge[0] in self.edges: continue
			self.edges[edge[0]] = Edge(edge[0], self, (self.getVertice(edge[1][0]), self.getVertice(edge[1][1])))
	def generateDrawableEdges(self, size):
		self.drawableEdges = [tuple(point.rpos*size for point in self.edges[key]) for key in self.edges]
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