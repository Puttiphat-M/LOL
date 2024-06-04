import os
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QApplication
from PySide6.QtGui import QPixmap, QPainter, QFont


class DonatePage(QWidget):
    def __init__(self):
        super().__init__()
        self.set_full_screen()
        self.timeout_count = 5
        font_size = int((self.width() + self.height()) / 10)
        script_dir = os.path.dirname(os.path.abspath(__file__))

        self.background_pixmap = QPixmap(os.path.join(script_dir, u"../resources/LotusBackground.jpg"))

        self.thankyou_label1 = QLabel("ขอขอบคุณ")
        self.thankyou_label1.setFont(QFont("Lotuss Smart HL", int(font_size), QFont.Bold))
        self.thankyou_label1.setStyleSheet("color: rgb(1, 187, 181);")
        self.thankyou_label1.setAlignment(Qt.AlignCenter)

        self.thankyou_label2 = QLabel("สำหรับการบริจาค")
        self.thankyou_label2.setFont(QFont("Lotuss Smart HL", int(font_size), QFont.Bold))
        self.thankyou_label2.setStyleSheet("color: rgb(1, 187, 181);")
        self.thankyou_label2.setAlignment(Qt.AlignCenter)

        self.logo_label_footer = QLabel()
        self.logo_pixmap = QPixmap(os.path.join(script_dir, u"../resources/Lotus.png"))
        self.logo_label_footer.setPixmap(self.logo_pixmap)
        self.logo_label_footer.setStyleSheet("background-color: transparent;")

        thankyou_layout = QVBoxLayout()
        thankyou_layout.addWidget(self.thankyou_label1, alignment=Qt.AlignCenter)
        thankyou_layout.addWidget(self.thankyou_label2, alignment=Qt.AlignCenter)
        thankyou_layout.setContentsMargins(20, 0, 20, 0)

        widget = QWidget()
        widget.setLayout(thankyou_layout)
        widget.setStyleSheet("background-color: white;")

        footer_layout = QHBoxLayout()
        footer_layout.addStretch(1)
        footer_layout.addWidget(self.logo_label_footer)

        self.footer_container = QWidget()
        self.footer_container.setLayout(footer_layout)
        self.footer_container.setStyleSheet("background-color: white;")

        main_layout = QVBoxLayout(self)
        main_layout.addStretch(1)
        main_layout.addWidget(widget, alignment=Qt.AlignCenter)
        main_layout.addStretch(1)
        main_layout.addWidget(self.footer_container)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.go_to_start_page_after_timeout)
        self.timer.start(1000)

        self.setWindowTitle("Donate Page")
        self.setStyleSheet("background-color: white;")
        self.setMinimumSize(640, 500)
        self.update_background()
        self.show()

    def update_background(self):
        self.background_pixmap = self.background_pixmap.scaled(self.width(), self.height())

    def go_to_start_page_after_timeout(self):
        from System.LotusSystem import LotusSystem
        self.timeout_count -= 1
        if self.timeout_count <= 0:
            LotusSystem.set_page("StartPage")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.background_pixmap)

    def set_full_screen(self):
        screen_geometry = QApplication.primaryScreen().geometry()
        self.setGeometry(screen_geometry)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.updateUI()

    def updateUI(self):
        thankyou_font_size = int((self.width() + self.height()) / 15)
        self.thankyou_label1.setFont(QFont("Lotuss Smart HL", thankyou_font_size, QFont.Bold))
        self.thankyou_label2.setFont(QFont("Lotuss Smart HL", thankyou_font_size, QFont.Bold))
        self.logo_label_footer.setPixmap(
            self.logo_pixmap.scaled(self.width() / 6.4, self.height() / 15, Qt.KeepAspectRatio))
