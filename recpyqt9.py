import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QGraphicsItem, QWidget, QPushButton


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(30,30,600,400)
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.rects = []
        
        # Create undo and redo buttons
        self.undo_btn = QPushButton('Undo', self)
        self.undo_btn.setGeometry(10, 10, 75, 30)
        self.undo_btn.clicked.connect(self.undo)
        
        self.redo_btn = QPushButton('Redo', self)
        self.redo_btn.setGeometry(95, 10, 75, 30)
        self.redo_btn.clicked.connect(self.redo)
        
        self.show()

    def paintEvent(self, event):
        qp = QPainter(self)
        for rect in self.rects:
            qp.setPen(QPen(Qt.red, 3))
            qp.drawRect(rect)
        if not self.begin.isNull() and not self.end.isNull():
            qp.setPen(QPen(Qt.blue, 3))
            qp.drawRect(QRectF(self.begin, self.end))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.begin = event.pos()
            self.end = event.pos()
            self.update()

    def mouseMoveEvent(self, event):
        if event.buttons() and Qt.LeftButton:
            self.end = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.rects.append(QRectF(self.begin, self.end))
            self.begin = QtCore.QPoint()
            self.end = QtCore.QPoint()
            self.update()
    
    def undo(self):
        if self.rects:
            self.rects.pop()
            self.update()
    
    def redo(self):
        if self.rects:
            self.rects.append(self.rects.pop())
            self.update()

        
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWidget()
    window.show()
    app.aboutToQuit.connect(app.deleteLater)
    sys.exit(app.exec_())

