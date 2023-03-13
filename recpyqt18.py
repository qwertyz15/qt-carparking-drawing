import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QPainter, QBrush, QColor, QPen, QPixmap
from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QGraphicsItem, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QWidget, QListWidget, QListWidgetItem


class Canvas(QtWidgets.QWidget):
    rectangle_added = QtCore.pyqtSignal(QRectF)

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
        # rint(len(self.rect_list))

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
                self.rectangle_added.emit(rect)
                self.undo_list.append(('add', rect))
                self.redo_list.clear()
                self.update()
            self.begin = QtCore.QPoint()
            self.end = QtCore.QPoint()
            print(len(self.rect_list))

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
            print(len(self.rect_list))

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
            print(len(self.rect_list))


class RectangleInfoWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.rect_list_widget = QListWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Rectangle List"))
        layout.addWidget(self.rect_list_widget)
        self.setLayout(layout)

    def add_rectangle(self, rect):
        item_text = f"({rect.x()}, {rect.y()}) - ({rect.x() + rect.width()}, {rect.y() + rect.height()})"
        self.rect_list_widget.addItem(item_text)

    def remove_rectangle(self):
        self.rect_list_widget.takeItem(self.rect_list_widget.count() - 1)


class MainWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.canvas = Canvas()
        self.image_label = QLabel()
        pixmap = QPixmap("example_image.png")
        self.image_label.setPixmap(pixmap)

        self.button_widget = QWidget()
        self.undo_button = QPushButton("Undo")
        self.undo_button.clicked.connect(self.canvas.undo)
        self.undo_button.clicked.connect(self.remove_rectangle)
        self.redo_button = QPushButton("Redo")
        self.redo_button.clicked.connect(self.canvas.redo)
        hbox = QHBoxLayout()
        hbox.addWidget(self.undo_button)
        hbox.addWidget(self.redo_button)
        self.button_widget.setLayout(hbox)

        self.rectangle_info_widget = RectangleInfoWidget()

        vbox = QVBoxLayout()
        vbox.addWidget(self.canvas, 1)
        vbox.addWidget(self.image_label, 4)

        hbox2 = QHBoxLayout()
        hbox2.addLayout(vbox)
        hbox2.addWidget(self.rectangle_info_widget)

        vbox2 = QVBoxLayout()
        vbox2.addLayout(hbox2)
        vbox2.addWidget(self.button_widget)
        self.setLayout(vbox2)

        self.canvas.rectangle_added.connect(self.on_rectangle_added)

    def on_rectangle_added(self, rect):
        self.rectangle_info_widget.add_rectangle(rect)

    def remove_rectangle(self):
        self.rectangle_info_widget.remove_rectangle()




if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QWidget()

    main_widget = MainWidget()

    vbox = QVBoxLayout()
    vbox.addWidget(main_widget)
    window.setLayout(vbox)

    window.show()
    app.aboutToQuit.connect(app.deleteLater)
    sys.exit(app.exec_())


       

