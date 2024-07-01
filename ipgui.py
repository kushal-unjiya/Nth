# #i want to make simple python gui based on pyqt5 in which user upload images from local machine like jpeg,jpg,png etc then user can apply image processing techniques with two different button grayscale and rbga then save the image in local machine.

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
        self.setGeometry(100, 100, 900, 700)

        self.image_label = QLabel(self)
        self.image_label.setGeometry(50, 50, 800, 400)

        self.upload_button = QPushButton('Upload Image', self)
        self.upload_button.setGeometry(50, 500, 150, 50)
        self.upload_button.clicked.connect(self.upload_image)

        self.grayscale_button = QPushButton('Grayscale', self)
        self.grayscale_button.setGeometry(250, 500, 150, 50)
        self.grayscale_button.clicked.connect(self.grayscale_image)

        self.rgba_button = QPushButton('RGBA', self)
        self.rgba_button.setGeometry(450, 500, 150, 50)
        self.rgba_button.clicked.connect(self.rgba_image)

        self.edge_button = QPushButton('Edge Detection', self)
        self.edge_button.setGeometry(50, 570, 150, 50)
        self.edge_button.clicked.connect(self.edge_detection)

        self.reset_button = QPushButton('Reset', self)
        self.reset_button.setGeometry(250, 570, 150, 50)
        self.reset_button.clicked.connect(self.reset_image)

        self.undo_button = QPushButton('Undo', self)
        self.undo_button.setGeometry(450, 570, 150, 50)
        self.undo_button.clicked.connect(self.undo_image)

        self.redo_button = QPushButton('Redo', self)
        self.redo_button.setGeometry(650, 570, 150, 50)
        self.redo_button.clicked.connect(self.redo_image)

        self.save_button = QPushButton('Save Image', self)
        self.save_button.setGeometry(650, 500, 150, 50)
        self.save_button.clicked.connect(self.save_image)

        self.image = None
        self.image_path = None
        self.image_history = []
        self.history_index = -1

        self.show()

    def upload_image(self):
        self.image_path, _ = QFileDialog.getOpenFileName(self, 'Open Image', '', 'Image Files (*.png *.jpg *.jpeg *.bmp)')
        if self.image_path:
            self.image = cv2.imread(self.image_path)
            self.image_history = [self.image.copy()]
            self.history_index = 0
            self.display_image()

    def display_image(self):
        if self.image is not None:
            if len(self.image.shape) == 2:
                image = cv2.cvtColor(self.image, cv2.COLOR_GRAY2RGB)
            else:
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
            self._add_to_history()
            self.display_image()

    def rgba_image(self):
        if self.image is not None:
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGBA)
            self._add_to_history()
            self.display_image()

    def edge_detection(self):
        if self.image is not None:
            gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY) if len(self.image.shape) == 3 else self.image
            edges = cv2.Canny(gray, 100, 200)
            self.image = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
            self._add_to_history()
            self.display_image()

    def reset_image(self):
        if self.image_history:
            self.image = self.image_history[0].copy()
            self.history_index = 0
            self.display_image()

    def undo_image(self):
        if self.history_index > 0:
            self.history_index -= 1
            self.image = self.image_history[self.history_index].copy()
            self.display_image()

    def redo_image(self):
        if self.history_index < len(self.image_history) - 1:
            self.history_index += 1
            self.image = self.image_history[self.history_index].copy()
            self.display_image()

    def save_image(self):
        if self.image is not None:
            image_path, _ = QFileDialog.getSaveFileName(self, 'Save Image', '', 'Image Files (*.png *.jpg *.jpeg *.bmp)')
            if image_path:
                cv2.imwrite(image_path, self.image)
                msg_box = QMessageBox()
                msg_box.setWindowTitle('Image Processing')
                msg_box.setText('Image saved successfully!')
                msg_box.exec_()

    def _add_to_history(self):
        if self.history_index < len(self.image_history) - 1:
            self.image_history = self.image_history[:self.history_index + 1]
        self.image_history.append(self.image.copy())
        self.history_index += 1

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageProcessingGUI()
    sys.exit(app.exec_())
