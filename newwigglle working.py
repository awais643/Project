import sys
from PyQt5.QtWidgets import (
    QApplication, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QFileDialog, QSlider, QWidget, QMainWindow, QFrame
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QTransform, QImage
from PIL import Image

class WiggleApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Enhanced 3D Wiggle Stereoscopy")
        self.setGeometry(100, 100, 1000, 800)  # Increased window size for better image display

        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # UI Elements
        self.image_frame = QFrame()
        self.image_frame.setFrameShape(QFrame.StyledPanel)
        self.image_frame.setStyleSheet("border: 2px solid #cccccc; border-radius: 10px; background-color: #f9f9f9;")

        self.image_label = QLabel("Upload images to see stereo effect")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("font-size: 16px; color: #666;")

        self.image_frame_layout = QVBoxLayout()
        self.image_frame_layout.addWidget(self.image_label)
        self.image_frame.setLayout(self.image_frame_layout)

        self.upload_button1 = QPushButton("Upload Left Image")
        self.upload_button1.setStyleSheet("padding: 10px; font-size: 14px; background-color: #4CAF50; color: white; border: none; border-radius: 5px;")
        self.upload_button1.clicked.connect(self.upload_image1)

        self.upload_button2 = QPushButton("Upload Right Image")
        self.upload_button2.setStyleSheet("padding: 10px; font-size: 14px; background-color: #4CAF50; color: white; border: none; border-radius: 5px;")
        self.upload_button2.clicked.connect(self.upload_image2)

        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setMinimum(1)
        self.speed_slider.setMaximum(20)
        self.speed_slider.setValue(5)  # Default slower value
        self.speed_slider.setTickInterval(1)
        self.speed_slider.setTickPosition(QSlider.TicksBelow)

        self.speed_label = QLabel("Speed: 5")
        self.speed_label.setStyleSheet("font-size: 14px; color: #333;")
        self.speed_slider.valueChanged.connect(self.update_speed_label)

        self.start_button = QPushButton("Start Wiggle")
        self.start_button.setStyleSheet("padding: 10px; font-size: 14px; background-color: #2196F3; color: white; border: none; border-radius: 5px;")
        self.start_button.clicked.connect(self.start_wiggle)
        self.start_button.setEnabled(False)

        self.stop_button = QPushButton("Stop Wiggle")
        self.stop_button.setStyleSheet("padding: 10px; font-size: 14px; background-color: #f44336; color: white; border: none; border-radius: 5px;")
        self.stop_button.clicked.connect(self.stop_wiggle)
        self.stop_button.setEnabled(False)

        self.download_button = QPushButton("Download GIF")
        self.download_button.setStyleSheet("padding: 10px; font-size: 14px; background-color: #FF9800; color: white; border: none; border-radius: 5px;")
        self.download_button.clicked.connect(self.download_gif)
        self.download_button.setEnabled(False)

        # Layout
        control_layout = QHBoxLayout()
        control_layout.addWidget(self.upload_button1)
        control_layout.addWidget(self.upload_button2)
        control_layout.addWidget(self.speed_label)
        control_layout.addWidget(self.speed_slider)
        control_layout.addWidget(self.start_button)
        control_layout.addWidget(self.stop_button)
        control_layout.addWidget(self.download_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.image_frame)
        main_layout.addLayout(control_layout)

        self.central_widget.setLayout(main_layout)

        # Timer for animation
        self.timer = QTimer()
        self.timer.timeout.connect(self.animate_images)

        # Animation variables
        self.wiggle_speed = 5
        self.image1 = None
        self.image2 = None
        self.current_image = 1
        self.frames = []  # To store animation frames
        self.frame_size = (800, 800)  # High-resolution size for better image quality

    def upload_image1(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Left Image", "", "Images (*.png *.xpm *.jpg *.jpeg *.bmp)")
        if file_path:
            self.image1 = QPixmap(file_path)
            self.check_images()

    def upload_image2(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Right Image", "", "Images (*.png *.xpm *.jpg *.jpeg *.bmp)")
        if file_path:
            self.image2 = QPixmap(file_path)
            self.check_images()

    def check_images(self):
        if self.image1 and self.image2:
            self.image_label.setPixmap(self.image1)
            self.image_label.setScaledContents(True)
            self.image_label.setFixedSize(self.frame_size[0], self.frame_size[1])  # Use high-resolution size
            self.start_button.setEnabled(True)
            self.download_button.setEnabled(True)

    def update_speed_label(self, value):
        self.speed_label.setText(f"Speed: {value}")
        self.wiggle_speed = value

    def start_wiggle(self):
        self.timer.start(500 // (self.wiggle_speed * 2))  # Slower and smoother transition
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

    def stop_wiggle(self):
        self.timer.stop()
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

    def animate_images(self):
        transform = QTransform()

        if self.current_image == 1:
            transform.rotate(-1, Qt.YAxis)  # Subtle rotation for left image
            scaled_pixmap = self.image1.transformed(transform)
            scaled_pixmap = scaled_pixmap.scaled(self.frame_size[0], self.frame_size[1], Qt.KeepAspectRatio)  # High-resolution scaling
            self.image_label.setPixmap(scaled_pixmap)
            self.frames.append(self.pixmap_to_image(scaled_pixmap))
            self.current_image = 2
        else:
            transform.rotate(1, Qt.YAxis)  # Subtle rotation for right image
            scaled_pixmap = self.image2.transformed(transform)
            scaled_pixmap = scaled_pixmap.scaled(self.frame_size[0], self.frame_size[1], Qt.KeepAspectRatio)  # High-resolution scaling
            self.image_label.setPixmap(scaled_pixmap)
            self.frames.append(self.pixmap_to_image(scaled_pixmap))
            self.current_image = 1

    def pixmap_to_image(self, pixmap):
        image = pixmap.toImage()
        buffer = image.bits()
        buffer.setsize(image.byteCount())
        pil_image = Image.frombytes("RGBA", (image.width(), image.height()), bytes(buffer)).convert("RGB")
        return pil_image

    def download_gif(self):
        if not self.frames:
            return

        save_path, _ = QFileDialog.getSaveFileName(self, "Save Wiggle GIF", "", "GIF Files (*.gif)")
        if save_path:
            self.frames[0].save(
                save_path,
                save_all=True,
                append_images=self.frames[1:],
                duration=1000 // self.wiggle_speed,
                loop=0,
                optimize=False,
                palette=Image.ADAPTIVE
            )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WiggleApp()
    window.show()
    sys.exit(app.exec_())
