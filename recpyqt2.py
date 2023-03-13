import sys
from PyQt5 import QtWidgets, QtCore, QtGui


class MyView(QtWidgets.QGraphicsView):
    def __init__(self, scene):
        super().__init__(scene)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setDragMode(QtWidgets.QGraphicsView.RubberBandDrag)
        self.setScene(scene)


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(30,30,600,400)

        self.scene = QtWidgets.QGraphicsScene(self)
        self.view = MyView(self.scene)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.view)

        self.show()

    def mouseReleaseEvent(self, event):
        rect = QtCore.QRectF(self.view.mapToScene(self.view.dragStartPosition()), 
                             self.view.mapToScene(self.view.dragCurrentPosition()))
        rect_item = QtWidgets.QGraphicsRectItem(rect)
        rect_item.setBrush(QtGui.QBrush(QtGui.QColor(100, 10, 10, 40)))
        self.scene.addItem(rect_item)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWidget()
    window.show()
    app.aboutToQuit.connect(app.deleteLater)
    sys.exit(app.exec_())

