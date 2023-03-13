import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QGraphicsScene, QGraphicsView
from PyQt5.QtGui import QPainter, QPen, QBrush
from PyQt5.QtCore import *


class ParkingSlots(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Parking Slots")
        self.setGeometry(100, 100, 800, 600)

        # Create a graphics scene and view
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setSceneRect(0, 0, 800, 600)

        # Create a layout for the buttons
        self.layout = QVBoxLayout()

        # Create the undo button
        self.undo_btn = QPushButton("Undo")
        self.undo_btn.clicked.connect(self.undo)

        # Create the save button
        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.save)

        # Add the buttons to the layout
        self.layout.addWidget(self.undo_btn)
        self.layout.addWidget(self.save_btn)

        # Add the view and layout to the main window
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.view)
        self.main_layout.addLayout(self.layout)

        self.setLayout(self.main_layout)

        # Keep track of the rectangles drawn
        self.rectangles = []

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Create a rectangle with the mouse position as the top-left corner
            rect = QRectF(event.pos(), QSizeF(100, 100))

            # Add the rectangle to the scene and save it
            self.scene.addRect(rect, QPen(Qt.black), QBrush(Qt.white))
            self.rectangles.append(rect)

        elif event.button() == Qt.RightButton:
            # Remove the last rectangle drawn from the scene and from the list of rectangles
            if self.rectangles:
                rect = self.rectangles.pop()
                self.scene.removeItem(rect)

    def undo(self):
        # Remove the last rectangle drawn from the scene and from the list of rectangles
        if self.rectangles:
            rect = self.rectangles.pop()
            self.scene.removeItem(rect)

    def save(self):
        # Save the coordinates of each rectangle in a text file
        if self.rectangles:
            with open("parking_slots.txt", "w") as f:
                for rect in self.rectangles:
                    x, y = rect.topLeft().x(), rect.topLeft().y()
                    w, h = rect.width(), rect.height()
                    f.write(f"{x},{y},{w},{h}\n")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ParkingSlots()
    window.show()
    sys.exit(app.exec_())
# your code goes here
