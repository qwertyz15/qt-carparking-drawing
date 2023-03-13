import sys
import pickle
import os
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QPainter, QBrush, QColor, QPen, QPixmap
from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QGraphicsItem, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QWidget, QListWidget, QListWidgetItem
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QPainter, QPainterPath, QRegion
from PyQt5.QtCore import Qt, QRectF
import cv2


os.makedirs("occupied", exist_ok=True)
os.makedirs("unoccupied", exist_ok=True)

class Canvas(QtWidgets.QWidget):
    rectangle_added = QtCore.pyqtSignal(tuple)

    def __init__(self, rect_occu_list):
        super().__init__()
        self.image_window_width = 600
        self.image_window_height = 400
        self.setFixedSize(self.image_window_width, self.image_window_height)

        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.rect_list = [rct[0] for rct in rect_occu_list]
        self.undo_list = []
        self.redo_list = []

        self.rect_occu_list = rect_occu_list
        self.occupancy = ""
        self.original_image = QPixmap("hik.png")

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.setRenderHint(QtGui.QPainter.Antialiasing)

        # image = QtGui.QImage("hik.png")
        image = self.original_image.toImage()
        scaled_image = image.scaled(self.rect().size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)

        self.x_scale =  image.width() / self.image_window_width
        self.y_scale =  image.height() / self.image_window_height

        qp.drawImage(self.rect(), image)
        pen = QtGui.QPen(QtGui.QColor(255, 255, 255), 1)
        qp.setPen(pen)

        # Set the fill color and transparency of the rectangle
        brush_color = QtGui.QColor(0, 0, 0, 64)  # blackish transparent color
        brush = QtGui.QBrush(brush_color)
        qp.setBrush(brush)

        for index, rect in enumerate(self.rect_list):
            qp.drawRect(rect)

            # Fill the rectangle with the blackish transparent color
            qp.fillRect(rect, brush_color)

            label_text = str(index + 1)
            font_metrics = QtGui.QFontMetrics(qp.font())
            label_width = font_metrics.width(label_text)
            label_height = font_metrics.height()
            label_rect = QtCore.QRectF(rect.center().x() - label_width / 2, rect.center().y() - label_height / 2, label_width, label_height)

            # Set the text color to white
            text_color = QtGui.QColor(255, 255, 255)
            qp.setPen(text_color)

            if(self.occupancy):
                qp.drawText(label_rect, label_text)
            else:
                qp.drawText(label_rect, label_text)
            # print(self.occupancy)

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
                # Create a message box for selecting an option
                msg_box = QMessageBox()
                msg_box.setWindowTitle("Select Option")
                msg_box.setText("Choose an option:")
                
                msg_box.addButton("Unoccupied", QMessageBox.NoRole)
                msg_box.addButton("Occupied", QMessageBox.YesRole)
                msg_box.addButton("Close", QMessageBox.RejectRole)

                # Show the message box and get the selected option
                selected_option = msg_box.exec()

                if selected_option == 2:
                    print("cancel")
                    return

                # Add the selected option and rectangle to the undo list
                if selected_option == 1:
                    occupancy = True
                    self.occupancy = True
                    self.undo_list.append(('add', rect, True))
                elif selected_option == 0:
                    occupancy = False
                    self.occupancy = False
                    self.undo_list.append(('add', rect, False))


                rect_with_occupancy = (rect, occupancy)
                self.rect_list.append(rect)
                self.rect_occu_list.append((rect, occupancy))
                self.rectangle_added.emit(rect_with_occupancy)
                self.redo_list.clear()
                self.update()

            self.begin = QtCore.QPoint()
            self.end = QtCore.QPoint()


    def undo(self):
        if self.undo_list:
            action, rect, occupancy = self.undo_list.pop()
            if action == 'add':
                self.rect_list.remove(rect)
                self.rect_occu_list.pop()
                if occupancy:
                    self.redo_list.append(('add', rect, True))
                else:
                    self.redo_list.append(('add', rect, False))
            elif action == 'delete':
                self.rect_list.append(rect)
                self.rect_occu_list.append((rect, occupancy))
                if occupancy:
                    self.redo_list.append(('delete', rect, True))
                else:
                    self.redo_list.append(('delete', rect, False))
            self.update()

    def redo(self):
        if self.redo_list:
            action, rect, occupancy = self.redo_list.pop()
            if action == 'add':
                self.rect_list.append(rect)
                self.rect_occu_list.append((rect, occupancy))
                if occupancy:
                    self.undo_list.append(('add', rect, True))
                else:
                    self.undo_list.append(('add', rect, False))
            elif action == 'delete':
                self.rect_list.remove(rect)
                self.rect_occu_list.pop()
                if occupancy:
                    self.undo_list.append(('delete', rect, True))
                else:
                    self.undo_list.append(('delete', rect, False))

            self.update()

    def clear(self):
        self.rect_list.clear()
        self.undo_list.clear()
        self.redo_list.clear()
        self.rect_occu_list.clear()
        self.update()



    def save(self):
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", "", "Pickle Files (*.pickle)")
        filename_org = filename + '_' + 'org'
        filename_org1 = filename + '_' + 'org1'
        
        if filename:
            
            self.rect_list_toupled = []
            for i, (rect, occ) in enumerate(self.rect_occu_list):
                x = rect.x() * self.x_scale
                y = rect.y() * self.y_scale
                w = rect.width() * self.x_scale
                h = rect.height() * self.y_scale

                cropped_image = self.original_image.copy(int(x), int(y), int(w), int(h))
                output_dir = "occupied" if occ else "unoccupied"
                output_path = os.path.join(output_dir, f"slot_{i + 1}.png")
                cropped_image.save(output_path)

                self.rect_list_toupled.append(((x, y, w, h), occ))

            with open(filename, "wb") as f:
                pickle.dump(self.rect_list_toupled, f)
            with open(filename_org, "wb") as f:
                pickle.dump(self.rect_occu_list, f)
            with open(filename_org1, "wb") as f:
                pickle.dump(self.rect_list, f)
            QtWidgets.QApplication.quit()


class RectangleInfoWidget(QtWidgets.QWidget):
    def __init__(self, rect_occu_list):
        super().__init__()
        self.rect_occu_list_widget = rect_occu_list
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(2)
        self.table_widget.setHorizontalHeaderLabels(['Slot', 'Occupancy'])
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Parking-Slot List"))
        layout.addWidget(self.table_widget)
        self.setLayout(layout)
        if(len(self.rect_occu_list_widget) > 0):
            for rct in self.rect_occu_list_widget:
                self.add_row(rct)

        self.deleted_rect_items = []

    def add_row(self, rct):
        sno = self.table_widget.rowCount()
        self.table_widget.insertRow(sno)
        occupancy = rct[1]
        occu_text = ("Occupied" if occupancy else "Unoccupied")
        slot_item = QTableWidgetItem(str(f"Slot: {sno + 1}"))
        occu_item = QTableWidgetItem(occu_text)
        self.table_widget.setItem(sno, 0, slot_item)
        self.table_widget.setItem(sno, 1, occu_item)

    def add_rectangle(self, rect_with_occupancy):
        self.add_row(rect_with_occupancy)


    def remove_rectangle(self):
        deleted_row = []
        if self.table_widget.rowCount() > len(self.rect_occu_list_widget):
            for i in range(self.table_widget.columnCount()):
                deleted_row.append(self.table_widget.takeItem(self.table_widget.rowCount() - 1, i))
            self.deleted_rect_items.append(deleted_row)
            self.table_widget.removeRow(self.table_widget.rowCount() - 1)


    def redo_last_deleted_item(self):
        if self.deleted_rect_items:
            deleted_item = self.deleted_rect_items.pop()
            row_index = self.table_widget.rowCount()
            self.table_widget.insertRow(row_index)
            for column_index, item in enumerate(deleted_item):
                table_item = QTableWidgetItem(item.text())
                self.table_widget.setItem(row_index, column_index, table_item)


class MainWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        try:
            with open('test123_org', 'rb') as f:
                rect_occu_list = pickle.load(f)
        except:
            rect_occu_list = []
        self.canvas = Canvas(rect_occu_list)
        self.image_label = QLabel()
        pixmap = QPixmap("example_image.png")
        self.image_label.setPixmap(pixmap)

        self.rectangle_info_widget = RectangleInfoWidget(rect_occu_list)

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

    def on_rectangle_added(self, rect_with_occupancy):
        self.rectangle_info_widget.add_rectangle(rect_with_occupancy)

    def clear_canvas(self):
        self.canvas.rect_list.clear()
        self.canvas.undo_list.clear()
        self.canvas.redo_list.clear()
        self.rectangle_info_widget.table_widget.clearContents()
        self.rectangle_info_widget.table_widget.setRowCount(0)




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