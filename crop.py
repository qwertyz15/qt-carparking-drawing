import cv2
from PyQt5.QtCore import QRectF

# Load the image
image = cv2.imread("hik.png")

# Define the QRectF object
rect = QRectF(601.6, 379.8, 93.86666666666666, 104.4)

# Convert the QRectF object to a tuple of integers
x, y, w, h = int(rect.x()), int(rect.y()), int(rect.width()), int(rect.height())

# Crop the image using the values from the QRectF object
cropped_image = image[y:y+h, x:x+w]

# Display the cropped image
cv2.imshow("Cropped Image", cropped_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
