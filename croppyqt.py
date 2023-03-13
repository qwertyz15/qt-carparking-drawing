from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPixmap
import os

# Create a QGuiApplication instance
app = QApplication([])

# Load the image
image_path = "hik.png"
image = QPixmap(image_path)

# Create the output directories
os.makedirs("occupied", exist_ok=True)
os.makedirs("unoccupied", exist_ok=True)

# Loop over the rectangles and occupancy status
rectangles = [((695.4666666666667, 370.8, 96.0, 153.0), False),
              ((582.4, 376.2, 98.13333333333333, 142.20000000000002), True),
              ((480.0, 388.8, 87.46666666666667, 115.2), True),
              ((381.8666666666667, 394.2, 51.2, 165.6), False)]

for rect, is_occupied in rectangles:
    # Extract the coordinates from the rectangle tuple
    x, y, w, h = rect

    # Crop the image using the coordinates
    cropped_image = image.copy(int(x), int(y), int(w), int(h))

    # Determine the output directory based on the occupancy status
    output_dir = "occupied" if is_occupied else "unoccupied"

    # Save the cropped image to the appropriate output directory
    output_path = os.path.join(output_dir, f"{x}_{y}_{w}_{h}.png")
    cropped_image.save(output_path)

# Quit the QGuiApplication instance
app.quit()

