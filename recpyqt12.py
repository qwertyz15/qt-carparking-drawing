import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QPainter, QBrush, QColor, QPen
from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QGraphicsItem, QHBoxLayout, QVBoxLayout, QPushButton, QWidget


class Canvas(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 600, 400)
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.rect_list = []
        self.undo_list = []
        self.redo_list = []

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.setRenderHint(QtGui.QPainter.Antialiasing)
        br = QtGui.QBrush(QtGui.QColor(100, 10, 10, 40))  
        qp.setBrush(br)
        for rect in self.rect_list:
            qp.drawRect(rect)

        if self.begin and self.end:
            qp.drawRect(QtCore.QRect(self.begin, self.end))

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


class Buttons(QWidget):
    def __init__(self, canvas):
        super().__init__()
        self.canvas = canvas
        self.undo_button = QPushButton("Undo")
        self.undo_button.clicked.connect(self.canvas.undo)
        self.redo_button = QPushButton("Redo")
        self.redo_button.clicked.connect(self.canvas.redo)
        hbox = QHBoxLayout()
        hbox.addWidget(self.undo_button)
        hbox.addWidget(self.redo_button)
        self.setLayout(hbox)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    canvas = Canvas()
    buttons = Buttons(canvas)
    vbox = QVBoxLayout()
    vbox.addWidget(canvas)
    vbox.addWidget(buttons)
    window = QWidget()
    window.setLayout(vbox)
    window.show()
    app.aboutToQuit.connect(app.deleteLater)
    sys.exit(app.exec_())

