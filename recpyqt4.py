import sys
from PyQt5 import QtWidgets, QtCore, QtGui


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(30,30,600,400)
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.show()

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        br = QtGui.QBrush(QtGui.QColor(100, 10, 10, 40))  
        qp.setBrush(br)   
        qp.drawRect(QtCore.QRect(self.begin, self.end))       

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.begin = event.pos()
            self.end = event.pos()
            self.update()
            self.print_start_pos(event.pos())

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.end = event.pos()
            self.update()
            self.update_mouse_pos(event.pos())

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.begin = event.pos()
            self.end = event.pos()
            self.update()
            self.print_end_pos(event.pos())

    def update_mouse_pos(self, pos):
        self.setWindowTitle(f'Mouse position: {pos.x()}, {pos.y()}')

    def print_start_pos(self, pos):
        print(f'Starting position: {pos.x()}, {pos.y()}')

    def print_end_pos(self, pos):
        print(f'Ending position: {pos.x()}, {pos.y()}')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWidget()
    window.show()
    app.aboutToQuit.connect(app.deleteLater)
    sys.exit(app.exec_())

