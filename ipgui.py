#i want to make python gui based on pyqt5 in which user upload images from local machine like jpeg,jpg,png etc then user can apply different image processing techniques like grayscale, rbga, blur etc and then save the image in local machine.


# The following code is a basic example of how you could start building a GUI using PyQt5.

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QGroupBox, QRadioButton, QSpinBox, QSlider, QSpinBox, QVBoxLayout, QHBoxLayout, QGroupBox, QRadioButton, QSpinBox, QSlider, QSpinBox
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
import cv2
import numpy as np

class ImageProcessingGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Image Processing GUI')
        self.setGeometry(100, 100, 800, 600)

        self.image = None
        self.processed_image = None

        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        self.image_label = QLabel()
        self.layout.addWidget(self.image_label)

        self.load_button = QPushButton('Load Image')
        self.load_button.clicked.connect(self.load_image)
        self.layout.addWidget(self.load_button)

        self.process_button = QPushButton('Process Image')
        self.process_button.clicked.connect(self.process_image)
        self.layout.addWidget(self.process_button)

        self.save_button = QPushButton('Save Image')
        self.save_button.clicked.connect(self.save_image)
        self.layout.addWidget(self.save_button)

        self.setLayout(self.layout)

    def load_image(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter('Images (*.png *.jpg *.jpeg)')
        file_dialog.selectNameFilter('Images (*.png *.jpg *.jpeg)')

        if file_dialog.exec_():
            file_name = file_dialog.selectedFiles()[0]
            self.image = cv2.imread(file_name)
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            self.image = QImage(self.image.data, self.image.shape[1], self.image.shape[0], QImage.Format_RGB888)
            self.image = QPixmap.fromImage(self.image)
            self.image_label.setPixmap(self.image.scaled(self.image_label.size(), Qt.KeepAspectRatio))

    def process_image(self):
        if self.image is not None:
            self.processed_image = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)
            self.processed_image = cv2.cvtColor(self.processed_image, cv2.COLOR_GRAY2RGB)
            self.processed_image = QImage(self.processed_image.data, self.processed_image.shape[1], self.processed_image.shape[0], QImage.Format_RGB888)
            self.processed_image = QPixmap.fromImage(self.processed_image)
            self.image_label.setPixmap(self.processed_image.scaled(self.image_label.size(), Qt.KeepAspectRatio))

    def save_image(self):
        if self.processed_image is not None:
            file_dialog = QFileDialog()
            file_dialog.setNameFilter('Images (*.png *.jpg *.jpeg)')
            file_dialog.selectNameFilter('Images (*.png *.jpg *.jpeg)')

            if file_dialog.exec_():
                file_name = file_dialog.selectedFiles()[0]
                self.processed_image.save(file_name)
                print(f'Image saved as {file_name}')
                
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageProcessingGUI()
    window.show()
    sys.exit(app.exec_())
    
# Run the code and you should see a window with a button to load an image, a button to process the image, and a button to save the image. When you click the load image button, you should be able to select an image from your local machine. When you click the process image button, the image should be converted to grayscale. When you click the save image button, you should be able to save the processed image to your local machine.
# To add more image processing techniques, you can add more buttons and radio buttons for different techniques, and update the process_image method accordingly. For example, to add a blur effect, you can add a button for blurring, a spin box for the blur radius, and update the process_image method to apply the blur effect.
