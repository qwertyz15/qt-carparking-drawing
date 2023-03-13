import sys
import pickle
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QPainter, QBrush, QColor, QPen, QPixmap
from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QGraphicsItem, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QWidget, QListWidget, QListWidgetItem


class Canvas(QtWidgets.QWidget):
    rectangle_added = QtCore.pyqtSignal(QRectF)

    def __init__(self):
        super().__init__()
        self.image_window_width = 600
        self.image_window_height = 400
        self.setFixedSize(self.image_window_width, self.image_window_height)
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.rect_list = []
        self.undo_list = []
        self.redo_list = []

        # # Create the clear button
        # self.clear_button = QtWidgets.QPushButton("Clear", self)
        # self.clear_button.move(10, 10)
        # self.clear_button.clicked.connect(self.clear)

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.setRenderHint(QtGui.QPainter.Antialiasing)
        image = QtGui.QImage("hik.png")
        scaled_image = image.scaled(self.rect().size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)

        # Calculate the scale factor for adjusting the rectangle coordinates
        # self.x_scale =  image.width() / scaled_image.width()
        # self.y_scale =  image.height() / scaled_image.height()

        self.x_scale =  image.width() / self.image_window_width
        self.y_scale =  image.height() / self.image_window_height
        print(scaled_image.width(), scaled_image.height())
        print(image.width(), image.height())
        print(self.x_scale, self.y_scale)

        qp.drawImage(self.rect(), image)
        pen = QtGui.QPen(QtGui.QColor(55, 42, 191), 2)
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
                # Create a dialog for selecting an option
                popup = QtWidgets.QDialog(self)
                popup.setWindowTitle("Select Option")
                popup.setGeometry(10, 30, 200, 100)

                # Create the radio buttons and add them to the dialog
                occupied_radio = QtWidgets.QRadioButton("Occupied", popup)
                not_occupied_radio = QtWidgets.QRadioButton("Not Occupied", popup)
                occupied_radio.move(10, 20)
                not_occupied_radio.move(10, 40)

                # Create the button box and add it to the dialog
                button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel, QtCore.Qt.Horizontal, popup)
                button_box.move(10, 70)
                button_box.accepted.connect(lambda: self.handle_radio_button(occupied_radio.isChecked(), rect))
                button_box.rejected.connect(popup.reject)

                # Show the dialog and wait for it to be closed
                popup.exec()

            self.begin = QtCore.QPoint()
            self.end = QtCore.QPoint()

    def handle_radio_button(self, is_occupied, rect):
        if is_occupied:
            self.undo_list.append(('add', rect, True))
        else:
            self.undo_list.append(('add', rect, False))

        self.rect_list.append(rect)
        self.rectangle_added.emit(rect)
        self.redo_list.clear()
        self.update()

    def undo(self):
        if self.undo_list:
            action, rect, occupancy = self.undo_list.pop()
            if action == 'add':
                self.rect_list.remove(rect)
                if occupancy == True:
                    self.redo_list.append(('add', rect, True))
                else:
                    self.redo_list.append(('add', rect, False))
            elif action == 'delete':
                self.rect_list.append(rect)
                if occupancy == True:
                    self.redo_list.append(('delete', rect, True))
                else:
                    self.redo_list.append(('delete', rect, False))
            self.update()

    def redo(self):
        if self.redo_list:
            action, rect, occupancy = self.redo_list.pop()
            if action == 'add':
                self.rect_list.append(rect)
                if occupancy == True:
                    self.undo_list.append(('add', rect, True))
                else:
                    self.undo_list.append(('add', rect, False))
            elif action == 'delete':
                self.rect_list.remove(rect)
                if occupancy == True:
                    self.undo_list.append(('delete', rect, True))
                else:
                    self.undo_list.append(('delete', rect, False))

            self.update()


    def clear(self):
        self.rect_list.clear()
        self.undo_list.clear()
        self.redo_list.clear()
        self.update()


    def save(self):
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", "", "Pickle Files (*.pickle)")
        if filename:
            self.rect_list_toupled = [ (rect.x() * self.x_scale, rect.y() * self.y_scale, rect.width() * self.x_scale, rect.height() * self.y_scale) for rect in self.rect_list]
            with open(filename, "wb") as f:
                pickle.dump(self.rect_list_toupled, f)
            QtWidgets.QApplication.quit()


class RectangleInfoWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.rect_list_widget = QListWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Rectangle List"))
        layout.addWidget(self.rect_list_widget)
        self.setLayout(layout)

        self.deleted_rect_items = []

    def add_rectangle(self, rect):
        item_text = f"({rect.x()}, {rect.y()}) - ({rect.x() + rect.width()}, {rect.y() + rect.height()})"
        self.rect_list_widget.addItem(item_text)
        # print(self.rect_list_widget)

    def remove_rectangle(self):
        if self.rect_list_widget.count() > 0:
            item = self.rect_list_widget.takeItem(self.rect_list_widget.count() - 1)
            self.deleted_rect_items.append(item)

    def redo_last_deleted_item(self):
        if self.deleted_rect_items:
            item = self.deleted_rect_items.pop()
            self.rect_list_widget.addItem(item.text())


class MainWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.canvas = Canvas()
        self.image_label = QLabel()
        pixmap = QPixmap("example_image.png")
        self.image_label.setPixmap(pixmap)

        self.rectangle_info_widget = RectangleInfoWidget()

        self.button_widget = QWidget()
        self.undo_button = QPushButton("Undo")
        self.undo_button.clicked.connect(self.canvas.undo)
        self.undo_button.clicked.connect(self.rectangle_info_widget.remove_rectangle)
        self.redo_button = QPushButton("Redo")
        self.redo_button.clicked.connect(self.canvas.redo)
        self.redo_button.clicked.connect(self.rectangle_info_widget.redo_last_deleted_item)
        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.canvas.clear)
        self.clear_button.clicked.connect(self.clear_canvas)
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.canvas.save)
        # self.save_button.clicked.connect(self.clear_canvas)
        hbox = QHBoxLayout()
        hbox.addWidget(self.undo_button)
        hbox.addWidget(self.redo_button)
        hbox.addWidget(self.clear_button)
        hbox.addWidget(self.save_button)
        self.button_widget.setLayout(hbox)

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

    def clear_canvas(self):
        self.canvas.rect_list.clear()
        self.canvas.undo_list.clear()
        self.canvas.redo_list.clear()
        self.rectangle_info_widget.rect_list_widget.clear()








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


       
