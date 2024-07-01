#i want to make simple python gui based on pyqt5 in which user upload images from local machine like jpeg,jpg,png etc then user can apply image processing techniques with two different button grayscale and rbga then save the image in local machine.

#now i want to add edge detection algorithm like canny sobel etc then save the image in local machine.



import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QFileDialog, QMessageBox
from PyQt5.QtGui import QImage, QPixmap
import cv2
import numpy as np

class ImageProcessingGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Image Processing GUI')
        self.setGeometry(100, 100, 800, 600)

        self.image_label = QLabel(self)
        self.image_label.setGeometry(50, 50, 700, 400)

        self.upload_button = QPushButton('Upload Image', self)
        self.upload_button.setGeometry(50, 500, 150, 50)
        self.upload_button.clicked.connect(self.upload_image)

        self.grayscale_button = QPushButton('Grayscale', self)
        self.grayscale_button.setGeometry(250, 500, 150, 50)
        self.grayscale_button.clicked.connect(self.grayscale_image)

        self.rgba_button = QPushButton('RGBA', self)
        self.rgba_button.setGeometry(450, 500, 150, 50)
        self.rgba_button.clicked.connect(self.rgba_image)

        self.save_button = QPushButton('Save Image', self)
        self.save_button.setGeometry(650, 500, 150, 50)
        self.save_button.clicked.connect(self.save_image)

        self.image = None
        self.image_path = None

        self.show()

    def upload_image(self):
        self.image_path, _ = QFileDialog.getOpenFileName(self, 'Open Image', '', 'Image Files (*.png *.jpg *.jpeg *.bmp)')
        self.image = cv2.imread(self.image_path)
        self.display_image()

    def display_image(self):
        image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        height, width, channel = image.shape
        bytesPerLine = 3 * width
        qImg = QImage(image.data, width, height, bytesPerLine, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qImg)
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)

    def grayscale_image(self):
        if self.image is not None:
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            self.display_image()

    def rgba_image(self):
        if self.image is not None:
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGBA)
            self.display_image()

    def save_image(self):
        if self.image is not None:
            image_path, _ = QFileDialog.getSaveFileName(self, 'Save Image', '', 'save Files (*.png *.jpg *.jpeg *.bmp)')
            cv2.imwrite(image_path, self.image)
            
            msg_box = QMessageBox()
            msg_box.setWindowTitle('Image Processing')
            msg_box.setText('Image saved successfully!')
            msg_box.exec_()
            
            self.image = None
            self.image_path = None
            self.display_image()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageProcessingGUI()
    sys.exit(app.exec_())
    