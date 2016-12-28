import drawSurface
import os
import sys
from PyQt5 import QtWidgets, QtGui, QtCore

class MainView(QtWidgets.QWidget):
	def __init__(self, parent=None):
		super(MainView, self).__init__(parent)

		botsplitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
		botsplitter.addWidget(drawSurface.DrawSurface())
		botsplitter.addWidget(drawSurface.DrawSurface())
		
		topsplitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)
		topsplitter.addWidget(botsplitter)
		
		vbox = QtWidgets.QVBoxLayout(self)
		
		vbox.addWidget(topsplitter)
		
		self.setLayout(vbox)

class MainWindow(QtWidgets.QMainWindow):
	def __init__(self, parent=None):
		super(MainWindow,self).__init__(parent)
		self.mainview = MainView()
		
		self.setCentralWidget(self.mainview)
		
		self.setWindowTitle('Test Hex Client')

		self.setGeometry(300, 300, 300, 200)

def test():
	app=QtWidgets.QApplication(sys.argv)
	w=MainWindow()
	w.show()
	sys.exit(app.exec_())
	
if __name__=='__main__': test()