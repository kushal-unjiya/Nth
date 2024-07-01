# #i want to make simple python gui based on pyqt5 in which user upload images from local machine like jpeg,jpg,png etc then user can apply image processing techniques with two different button grayscale and rbga then save the image in local machine.
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QFileDialog, QMessageBox, QVBoxLayout, QHBoxLayout, QGridLayout, QScrollArea
)
from PyQt5.QtGui import QImage, QPixmap
import cv2
import numpy as np
import math

class ImageProcessingGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Image Processing GUI')
        self.setGeometry(100, 100, 1200, 800)

        # Main layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget(self.scroll_area)
        self.scroll_layout = QGridLayout(self.scroll_content)
        self.scroll_content.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_content)
        self.layout.addWidget(self.scroll_area)

        # Button layout
        button_layout = QHBoxLayout()
        self.layout.addLayout(button_layout)

        # Upload button
        self.upload_button = QPushButton('Upload Images', self)
        self.upload_button.clicked.connect(self.upload_images)
        button_layout.addWidget(self.upload_button)

        # Grayscale button
        self.grayscale_button = QPushButton('Grayscale', self)
        self.grayscale_button.clicked.connect(self.grayscale_image)
        button_layout.addWidget(self.grayscale_button)

        # RGBA button
        self.rgba_button = QPushButton('RGBA', self)
        self.rgba_button.clicked.connect(self.rgba_image)
        button_layout.addWidget(self.rgba_button)

        # Edge detection button
        self.edge_button = QPushButton('Edge Detection', self)
        self.edge_button.clicked.connect(self.edge_detection)
        button_layout.addWidget(self.edge_button)

        # Denoise button
        self.denoise_button = QPushButton('Denoise', self)
        self.denoise_button.clicked.connect(self.denoise_image)
        button_layout.addWidget(self.denoise_button)

        # Blur button
        self.blur_button = QPushButton('Blur', self)
        self.blur_button.clicked.connect(self.blur_image)
        button_layout.addWidget(self.blur_button)

        # Sharpen button
        self.sharpen_button = QPushButton('Sharpen', self)
        self.sharpen_button.clicked.connect(self.sharpen_image)
        button_layout.addWidget(self.sharpen_button)

        # Rotate button
        self.rotate_button = QPushButton('Rotate', self)
        self.rotate_button.clicked.connect(self.rotate_image)
        button_layout.addWidget(self.rotate_button)

        # Flip button
        self.flip_button = QPushButton('Flip', self)
        self.flip_button.clicked.connect(self.flip_image)
        button_layout.addWidget(self.flip_button)

        # Reset button
        self.reset_button = QPushButton('Reset', self)
        self.reset_button.clicked.connect(self.reset_image)
        button_layout.addWidget(self.reset_button)

        # Undo button
        self.undo_button = QPushButton('Undo', self)
        self.undo_button.clicked.connect(self.undo_image)
        button_layout.addWidget(self.undo_button)

        # Redo button
        self.redo_button = QPushButton('Redo', self)
        self.redo_button.clicked.connect(self.redo_image)
        button_layout.addWidget(self.redo_button)

        # Save button
        self.save_button = QPushButton('Save Images', self)
        self.save_button.clicked.connect(self.save_images)
        button_layout.addWidget(self.save_button)

        self.images = []
        self.original_images = []
        self.image_labels = []
        self.image_histories = []
        self.history_indices = []
        self.zoom_levels = []

        self.show()

    def upload_images(self):
        image_paths, _ = QFileDialog.getOpenFileNames(self, 'Open Images', '', 'Image Files (*.png *.jpg *.jpeg *.bmp)')
        if image_paths:
            self.clear_images()
            for image_path in image_paths:
                image = cv2.imread(image_path)
                self.images.append(image)
                self.original_images.append(image.copy())
                self.image_histories.append([image.copy()])
                self.history_indices.append(0)
                self.zoom_levels.append(1)
                
                image_label = QLabel(self)
                self.image_labels.append(image_label)
                self.scroll_layout.addWidget(image_label)
            
            self.display_images()

    def display_images(self):
        num_images = len(self.images)
        num_columns = 3  # Change this value to arrange images in more or fewer columns
        num_rows = math.ceil(num_images / num_columns)

        for i, image in enumerate(self.images):
            if len(image.shape) == 2:
                display_image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
            else:
                display_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            height, width, channel = display_image.shape
            bytesPerLine = 3 * width
            qImg = QImage(display_image.data, width, height, bytesPerLine, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qImg)

            max_width = 300
            max_height = 300
            scaled_pixmap = pixmap.scaled(max_width, max_height, aspectRatioMode=True)
            self.image_labels[i].setPixmap(scaled_pixmap)
            self.image_labels[i].setFixedSize(max_width, max_height)
            self.image_labels[i].setScaledContents(True)

            row = i // num_columns
            col = i % num_columns
            self.scroll_layout.addWidget(self.image_labels[i], row, col)

    def grayscale_image(self):
        self._apply_to_all_images(lambda img: cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))

    def rgba_image(self):
        self._apply_to_all_images(lambda img: cv2.cvtColor(img, cv2.COLOR_BGR2RGBA))

    def edge_detection(self):
        def detect_edges(img):
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img
            edges = cv2.Canny(gray, 100, 200)
            return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        
        self._apply_to_all_images(detect_edges)

    def denoise_image(self):
        self._apply_to_all_images(lambda img: cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21))

    def blur_image(self):
        self._apply_to_all_images(lambda img: cv2.GaussianBlur(img, (5, 5), 0))

    def sharpen_image(self):
        def sharpen(img):
            kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
            return cv2.filter2D(img, -1, kernel)
        
        self._apply_to_all_images(sharpen)

    def rotate_image(self):
        self._apply_to_all_images(lambda img: cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE))

    def flip_image(self):
        self._apply_to_all_images(lambda img: cv2.flip(img, 1))

    def reset_image(self):
        for i in range(len(self.images)):
            self.images[i] = self.original_images[i].copy()
            self.image_histories[i] = [self.images[i].copy()]
            self.history_indices[i] = 0
            self.zoom_levels[i] = 1
        self.display_images()

    def undo_image(self):
        for i in range(len(self.images)):
            if self.history_indices[i] > 0:
                self.history_indices[i] -= 1
                self.images[i] = self.image_histories[i][self.history_indices[i]].copy()
        self.display_images()

    def redo_image(self):
        for i in range(len(self.images)):
            if self.history_indices[i] < len(self.image_histories[i]) - 1:
                self.history_indices[i] += 1
                self.images[i] = self.image_histories[i][self.history_indices[i]].copy()
        self.display_images()

    def save_images(self):
        save_dir = QFileDialog.getExistingDirectory(self, 'Save Images', '')
        if save_dir:
            for i, image in enumerate(self.images):
                save_path = f"{save_dir}/image_{i}.png"
                cv2.imwrite(save_path, image)
            
            msg_box = QMessageBox()
            msg_box.setWindowTitle('Image Processing')
            msg_box.setText('Images saved successfully!')
            msg_box.exec_()

    def _apply_to_all_images(self, func):
        for i in range(len(self.images)):
            self.images[i] = func(self.images[i])
            self._add_to_history(i)
        self.display_images()

    def _add_to_history(self, index):
        if self.history_indices[index] < len(self.image_histories[index]) - 1:
            self.image_histories[index] = self.image_histories[index][:self.history_indices[index] + 1]
        self.image_histories[index].append(self.images[index].copy())
        self.history_indices[index] += 1

    def clear_images(self):
        for label in self.image_labels:
            self.scroll_layout.removeWidget(label)
            label.deleteLater()
        self.image_labels.clear()
        self.images.clear()
        self.original_images.clear()
        self.image_histories.clear()
        self.history_indices.clear()
        self.zoom_levels.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageProcessingGUI()
    sys.exit(app.exec_())
