import sys
from PyQt5 import QtWidgets, QtCore, QtGui


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(30, 30, 600, 400)
        self.rectangles = []
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.show()

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        br = QtGui.QBrush(QtGui.QColor(100, 10, 10, 40))
        qp.setBrush(br)
        for rect in self.rectangles:
            qp.drawRect(rect)
        if self.begin and self.end:
            temp_rect = QtCore.QRectF(self.begin, self.end)
            qp.drawRect(temp_rect)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.begin = event.pos()
            self.end = event.pos()
            self.update()

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.end = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            rect = QtCore.QRectF(self.begin, self.end)
            self.rectangles.append(rect)
            self.begin = QtCore.QPoint()
            self.end = QtCore.QPoint()
            self.update()
            print("Starting position: ", self.rectangles[-1].topLeft())
            print("Ending position: ", self.rectangles[-1].bottomRight())


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWidget()
    window.show()
    app.aboutToQuit.connect(app.deleteLater)
    sys.exit(app.exec_())

