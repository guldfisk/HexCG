from PyQt5 import QtWidgets, QtGui, QtCore
from hexGrid import *

class DrawableHex(Hex):
	def draw(self, painter, ox, oy):
		s = ''.join(str(item)+'\n' for item in self.borderPositions)
		rect = painter.boundingRect(QtCore.QRectF(), 0, s)
		rect.moveCenter(QtCore.QPointF(*self.rcCenter*40+(ox, oy)))
		painter.drawText(rect, s)

class DrawSurface(QtWidgets.QWidget):
	def __init__(self, parent=None):
		super(DrawSurface, self).__init__(parent)
		self.setMinimumSize(1, 1)
		self.pen = QtGui.QPen()
		self.pen.setColor(QtGui.QColor(0, 0, 0))
		self.pen.setWidth(1)
		self.map = HexMap(DrawableHex)
		self.map.makeFromMovementRange(4)
		self.map.generateDrawableEdges(40)
	def paintEvent(self, event):
		x, y = self.size().width(), self.size().height()
		hx, hy = x/2, y/2
		qp=QtGui.QPainter()
		qp.begin(self)
		qp.setPen(self.pen)
		# print(self.map.drawableEdges)
		# print(self.map.drawableEdges)
		for edge in self.map.drawableEdges:
			qp.drawLine(edge[0][0]+hx, edge[0][1]+hy, edge[1][0]+hx, edge[1][1]+hy)
		for key in self.map: self.map[key].draw(qp, hx, hy)
		qp.end()