import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QPainter, QBrush, QColor, QPen
from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QGraphicsItem, QHBoxLayout, QVBoxLayout, QPushButton

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(30,30,600,400)
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.rect_list = []
        self.undo_list = []
        self.redo_list = []
        self.undo_button = QPushButton("Undo")
        self.undo_button.clicked.connect(self.undo)
        self.redo_button = QPushButton("Redo")
        self.redo_button.clicked.connect(self.redo)
        hbox = QHBoxLayout()
        hbox.addWidget(self.undo_button)
        hbox.addWidget(self.redo_button)
        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        self.setLayout(vbox)
        self.show()

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.setRenderHint(QtGui.QPainter.Antialiasing)
        br = QtGui.QBrush(QtGui.QColor(100, 10, 10, 40))  
        qp.setBrush(br)
        for rect in self.rect_list:
            qp.drawRect(rect)
        if not self.begin.isNull() and not self.end.isNull():
            qp.drawRect(QtCore.QRectF(self.begin, self.end))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.begin = event.pos()
            self.end = event.pos()
            self.update()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.end = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            rect = QRectF(self.begin, self.end)
            if rect.width() > 0 and rect.height() > 0:
                self.rect_list.append(rect)
                self.undo_list.append(('add', rect))
                self.redo_list.clear()
                self.update()
            self.begin = QtCore.QPoint()
            self.end = QtCore.QPoint()

    def undo(self):
        if self.undo_list:
            action, rect = self.undo_list.pop()
            if action == 'add':
                self.rect_list.remove(rect)
                self.redo_list.append(('add', rect))
            elif action == 'delete':
                self.rect_list.append(rect)
                self.redo_list.append(('delete', rect))
            self.update()

    def redo(self):
        if self.redo_list:
            action, rect = self.redo_list.pop()
            if action == 'add':
                self.rect_list.append(rect)
                self.undo_list.append(('add', rect))
            elif action == 'delete':
                self.rect_list.remove(rect)
                self.undo_list.append(('delete', rect))
            self.update()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWidget()
    window.show()
    app.aboutToQuit.connect(app.deleteLater)
    sys.exit(app.exec_())

