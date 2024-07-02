# #i want to make simple python gui based on pyqt5 in which user upload images from local machine like jpeg,jpg,png etc then user can apply image processing techniques with two different button grayscale and rbga then save the image in local machine.
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QAction, QFileDialog, QLabel, QVBoxLayout, QGridLayout, QScrollArea, QWidget, QStatusBar
)
from PyQt5.QtGui import QImage, QPixmap, QPalette, QLinearGradient, QColor, QFont
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect
import cv2
import numpy as np
import math

class ImageProcessingGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Image Processing GUI')
        self.setGeometry(100, 100, 1200, 800)

        # Set a gradient background for the main window
        palette = QPalette()
        gradient = QLinearGradient(0, 0, 0, 1)
        gradient.setCoordinateMode(QLinearGradient.ObjectBoundingMode)
        gradient.setColorAt(0.0, QColor(255, 140, 0))
        gradient.setColorAt(1.0, QColor(255, 69, 0))
        palette.setBrush(QPalette.Window, gradient)
        self.setPalette(palette)

        # Central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget(self.scroll_area)
        self.scroll_layout = QGridLayout(self.scroll_content)
        self.scroll_content.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_content)
        self.layout.addWidget(self.scroll_area)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.create_menu()

        self.images = []
        self.original_images = []
        self.image_labels = []
        self.image_histories = []
        self.history_indices = []
        self.zoom_levels = []

        self.setStyleSheet(self.load_stylesheet())
        self.show()

    def create_menu(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu('File')
        process_menu = menubar.addMenu('Process')
        tools_menu = menubar.addMenu('Tools')

        upload_action = QAction('Upload Images', self)
        upload_action.triggered.connect(self.upload_images)
        file_menu.addAction(upload_action)

        save_action = QAction('Save Images', self)
        save_action.triggered.connect(self.save_images)
        file_menu.addAction(save_action)

        grayscale_action = QAction('Grayscale', self)
        grayscale_action.triggered.connect(self.grayscale_image)
        process_menu.addAction(grayscale_action)

        rgba_action = QAction('RGBA', self)
        rgba_action.triggered.connect(self.rgba_image)
        process_menu.addAction(rgba_action)

        edge_action = QAction('Edge Detection', self)
        edge_action.triggered.connect(self.edge_detection)
        process_menu.addAction(edge_action)

        denoise_action = QAction('Denoise', self)
        denoise_action.triggered.connect(self.denoise_image)
        process_menu.addAction(denoise_action)

        blur_action = QAction('Blur', self)
        blur_action.triggered.connect(self.blur_image)
        process_menu.addAction(blur_action)

        sharpen_action = QAction('Sharpen', self)
        sharpen_action.triggered.connect(self.sharpen_image)
        process_menu.addAction(sharpen_action)

        rotate_action = QAction('Rotate', self)
        rotate_action.triggered.connect(self.rotate_image)
        process_menu.addAction(rotate_action)

        flip_action = QAction('Flip', self)
        flip_action.triggered.connect(self.flip_image)
        process_menu.addAction(flip_action)

        template_action = QAction('Template Matching', self)
        template_action.triggered.connect(self.template_matching)
        tools_menu.addAction(template_action)
        
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
            scaled_pixmap = pixmap.scaled(max_width, max_height, Qt.KeepAspectRatio)
            self.image_labels[i].setPixmap(scaled_pixmap)
            self.image_labels[i].setFixedSize(max_width, max_height)
            self.image_labels[i].setScaledContents(True)

            row = i // num_columns
            col = i % num_columns
            self.scroll_layout.addWidget(self.image_labels[i], row, col)

            self.animate_image(self.image_labels[i], i)

    def animate_image(self, label, index):
        anim = QPropertyAnimation(label, b"geometry")
        anim.setDuration(1000)
        anim.setStartValue(QRect(label.x(), label.y() - 100, label.width(), label.height()))
        anim.setEndValue(QRect(label.x(), label.y(), label.width(), label.height()))
        anim.start()

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

    def template_matching(self):
        template_path, _ = QFileDialog.getOpenFileName(self, 'Open Template Image', '', 'Image Files (*.png *.jpg *.jpeg *.bmp)')
        if template_path:
            template = cv2.imread(template_path, 0)
            for i in range(len(self.images)):
                img_gray = cv2.cvtColor(self.images[i], cv2.COLOR_BGR2GRAY)
                w, h = template.shape[::-1]
                res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
                threshold = 0.8
                loc = np.where(res >= threshold)
                rectangles = []
                for pt in zip(*loc[::-1]):
                    rectangles.append([int(pt[0]), int(pt[1]), int(w), int(h)])
                rectangles, _ = cv2.groupRectangles(rectangles, 1, 0.2)

                for (x, y, w, h) in rectangles:
                    cv2.rectangle(self.images[i], (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            self.display_images()

    def save_images(self):
        for i, image in enumerate(self.images):
            save_path, _ = QFileDialog.getSaveFileName(self, 'Save Image', f'image_{i}.png', 'Image Files (*.png *.jpg *.jpeg *.bmp)')
            if save_path:
                cv2.imwrite(save_path, image)

    def clear_images(self):
        for image_label in self.image_labels:
            self.scroll_layout.removeWidget(image_label)
            image_label.deleteLater()
        self.images = []
        self.original_images = []
        self.image_labels = []
        self.image_histories = []
        self.history_indices = []
        self.zoom_levels = []

    def _apply_to_all_images(self, func):
        for i in range(len(self.images)):
            self.images[i] = func(self.images[i])
            self._update_history(i)
        self.display_images()

    def _update_history(self, index):
        if self.history_indices[index] < len(self.image_histories[index]) - 1:
            self.image_histories[index] = self.image_histories[index][:self.history_indices[index] + 1]
        self.image_histories[index].append(self.images[index].copy())
        self.history_indices[index] += 1

    def load_stylesheet(self):
        return """
        QMainWindow {
            background-color: #2b2b2b;
            color: #ffffff;
        }
        QMenuBar {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #ff8c00, stop:1 #ff4500);
            color: #ffffff;
            font-size: 16px;
        }
        QMenuBar::item {
            background: transparent;
            color: #ffffff;
        }
        QMenuBar::item:selected {
            background: rgba(255, 255, 255, 30);
        }
        QMenu {
            background-color: #3c3f41;
            color: #ffffff;
            font-size: 16px;
        }
        QMenu::item:selected {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #ff8c00, stop:1 #ff4500);
        }
        QLabel {
            color: #ffffff;
            font-size: 14px;
        }
        QScrollArea {
            background-color: #2b2b2b;
        }
        QStatusBar {
            background-color: #3c3f41;
            color: #ffffff;
            font-size: 14px;
        }
        QPushButton {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #ff8c00, stop:1 #ff4500);
            color: #ffffff;
            border-radius: 8px;
            padding: 10px;
            font-size: 14px;
            font-weight: bold;
            transition: all 0.3s ease-in-out;
        }
        QPushButton:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #ff4500, stop:1 #ff8c00);
            transform: scale(1.05);
        }
        """

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageProcessingGUI()
    sys.exit(app.exec_())