import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QPainter, QBrush, QColor, QPen, QPixmap, QFontMetrics
from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QGraphicsItem, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QWidget

class Canvas(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(600, 400)
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.rect_list = []
        self.undo_list = []
        self.redo_list = []

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.setRenderHint(QtGui.QPainter.Antialiasing)
        image = QtGui.QImage("hik.png")
        qp.drawImage(self.rect(), image)
        pen = QtGui.QPen(QtGui.QColor(255, 0, 0), 2)
        qp.setPen(pen)
        for index, rect in enumerate(self.rect_list):
            qp.drawRect(rect)
            label_text = str(index + 1)
            font_metrics = QtGui.QFontMetrics(qp.font())
            label_width = font_metrics.width(label_text)
            label_height = font_metrics.height()
            label_rect = QtCore.QRectF(rect.center().x() - label_width / 2, rect.center().y() - label_height / 2, label_width, label_height)
            qp.drawText(label_rect, label_text)

        if self.begin and self.end:
            qp.drawRect(QtCore.QRect(self.begin, self.end))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.begin = event.pos()
            self.end = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.end = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            rect = QRectF(self.begin, self.end)
            startPoint = (self.begin.x(), self.begin.y())
            endPoint = (self.end.x(), self.end.y())
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
    window = QtWidgets.QWidget()

    canvas = Canvas()
    image_label = QLabel()
    pixmap = QPixmap("")
    image_label.setPixmap(pixmap)

    button_widget = QWidget()
    undo_button = QPushButton("Undo")
    undo_button.clicked.connect(canvas.undo)
    redo_button = QPushButton("Redo")
    redo_button.clicked.connect(canvas.redo)
    hbox = QHBoxLayout()
    hbox.addWidget(undo_button)
    hbox.addWidget(redo_button)
    button_widget.setLayout(hbox)

    vbox = QVBoxLayout()
    vbox.addWidget(canvas, 1)
    vbox.addWidget(image_label, 4)
    vbox.addWidget(button_widget)
    window.setLayout(vbox)

    window.show()
    app.aboutToQuit.connect(app.deleteLater)
    sys.exit(app.exec_())

