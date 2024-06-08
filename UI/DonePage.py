import io
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QApplication
from PySide6.QtGui import QPixmap, QFont, Qt, QImage, QPainter


class DonePage(QWidget):
    def __init__(self):
        super().__init__()
        self.set_full_screen()
        self.qr_image = None
        from UI.Component import resource_path
        self.background_pixmap = QPixmap(resource_path("resources/LotusBackground.jpg"))

        self.qr_label = QLabel("กรุณาสแกน QR เพื่อสะสมขวด")
        self.qr_label.setFont(QFont("Lotuss Smart HL", 22, QFont.Bold))
        self.qr_label.setStyleSheet("color: rgb(1, 187, 181);")
        self.qr_label.setAlignment(Qt.AlignCenter)

        self.logo_label_footer = QLabel()
        self.logo_pixmap = QPixmap(resource_path("resources/Lotus.png"))
        self.logo_label_footer.setPixmap(self.logo_pixmap)
        self.logo_label_footer.setStyleSheet("background-color: transparent;")

        self.qr = QLabel(self)
        self.qr.setStyleSheet("background-color: transparent;")

        qr_layout = QVBoxLayout()
        qr_layout.addWidget(self.qr_label)
        qr_layout.addSpacing(15)
        qr_layout.addWidget(self.qr)

        qr_widget = QWidget()
        qr_widget.setLayout(qr_layout)
        qr_widget.setStyleSheet("background-color: white;")

        footer_layout = QHBoxLayout()
        footer_layout.addStretch(1)
        footer_layout.addWidget(self.logo_label_footer)

        self.footer_container = QWidget()
        self.footer_container.setLayout(footer_layout)
        self.footer_container.setStyleSheet("background-color: white;")

        self.info_label = QLabel("ได้รับขวด")
        self.info_label.setFont(QFont("Lotuss Smart HL", 22))
        self.info_label.setStyleSheet('''
                            QLabel {
                                color: rgb(0, 0, 0);
                                background-color: transparent;
                            }
                        ''')

        from LotusSystem import LotusSystem
        self.count_label = QLabel(str(LotusSystem.get_bottle_count()))
        self.count_label.setFont(QFont("Lotuss Smart HL", 30))
        self.count_label.setStyleSheet('''
                                    QLabel {
                                        color: rgb(0, 0, 0);
                                        background-color: transparent;
                                    }
                                ''')

        self.bottle_logo = QLabel()
        self.bottle_logo.setStyleSheet("background-color: transparent;")
        self.bottle_pixmap = QPixmap(resource_path("resources/bottle.png"))
        self.bottle_logo.setPixmap(self.bottle_pixmap)

        self.done_button = QPushButton("เสร็จสิ้น")
        self.done_button.setFont(QFont("Lotuss Smart HL", 20, QFont.Bold))
        self.done_button.setStyleSheet('''
                            QPushButton {
                                color: rgb(255, 255, 255);
                                background-color: rgb(255, 196, 0);
                                border-radius: 20px;
                                border: none; /* Ensure no border */
                                padding: 5px; /* Adjust padding */
                            }
                        ''')
        self.done_button.clicked.connect(self.go_to_start_page)

        value_layout = QHBoxLayout()
        value_layout.addStretch(1)
        value_layout.addWidget(self.info_label)
        value_layout.addSpacing(5)
        value_layout.addWidget(self.count_label)
        value_layout.addSpacing(5)
        value_layout.addWidget(self.bottle_logo)
        value_layout.addStretch(1)

        right_layout = QVBoxLayout()
        right_layout.addSpacing(30)
        right_layout.addLayout(value_layout)
        right_layout.addStretch(1)
        right_layout.addWidget(self.done_button)

        leftright_layout = QHBoxLayout()
        leftright_layout.addStretch(1)
        leftright_layout.addWidget(qr_widget)
        leftright_layout.addStretch(1)
        leftright_layout.addLayout(right_layout)
        leftright_layout.addStretch(1)

        main_layout = QVBoxLayout(self)
        main_layout.addSpacing(45)
        main_layout.addLayout(leftright_layout)
        main_layout.addStretch(1)
        main_layout.addWidget(self.footer_container)
        main_layout.setContentsMargins(0, self.height() * 0.03, 0, 0)

        self.setWindowTitle("Done Page")
        self.setMinimumSize(640, 500)
        self.show_qr_code()
        self.show()

    def go_to_start_page(self):
        from LotusSystem import LotusSystem
        LotusSystem.set_page("StartPage")

    def show_qr_code(self):
        from LotusSystem import LotusSystem
        self.qr_image = LotusSystem.get_qr()

        byte_array = io.BytesIO()
        self.qr_image.save(byte_array, format='PNG')
        byte_array.seek(0)

        q_image = QImage.fromData(byte_array.getvalue())

        self.pixmap = QPixmap.fromImage(q_image)

        self.qr.setPixmap(self.pixmap)
        self.qr.setAlignment(Qt.AlignCenter)

    def set_full_screen(self):
        screen_geometry = QApplication.primaryScreen().geometry()
        self.setGeometry(screen_geometry)

    def paintEvent(self, event):
        from UI.Component import resource_path
        painter = QPainter(self)
        painter.drawPixmap(0, 0, QPixmap(resource_path("resources/LotusBackground.jpg")).scaled(self.width(), self.height()))
        painter.end()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.updateUI()

    def updateUI(self):
        button_width = int(self.width() * 0.2)
        button_height = int(self.height() * 0.08)
        width_ratio = self.width() / 640
        height_ratio = self.height() / 480
        bottle_size = int(25 * (width_ratio + height_ratio) / 2)
        self.bottle_logo.setPixmap(self.bottle_pixmap.scaled(bottle_size, bottle_size, Qt.KeepAspectRatio))
        self.qr.setPixmap(self.pixmap.scaled(self.width() / 1.8, self.height() / 1.8, Qt.KeepAspectRatio))
        self.qr_label.setFont(QFont("Lotuss Smart HL", int((self.width() + self.height()) / 50), QFont.Bold))
        self.count_label.setFont(QFont("Lotuss Smart HL", int((self.width() + self.height()) / 40)))
        self.info_label.setFont(QFont("Lotuss Smart HL", int((self.width() + self.height()) / 55)))
        self.logo_label_footer.setPixmap(self.logo_pixmap.scaled(self.width() / 6.4, self.height() / 15, Qt.KeepAspectRatio))
        self.done_button.setFont(QFont("Lotuss Smart HL", int((self.width() + self.height()) / 55), QFont.Bold))
        self.done_button.setFixedSize(button_width, button_height)
