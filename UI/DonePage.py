import os
import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton
from PySide6.QtGui import QPixmap, QPainter, QFont, Qt


class DonePage(QWidget):
    def __init__(self, lotus_system):
        super().__init__()
        self.lotus_system = lotus_system
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Load background image
        self.background_pixmap = QPixmap(os.path.join(script_dir, u"../resources/LotusBackground.jpg"))

        qr_label = QLabel("กรุณาสแกน QR เพื่อสะสมขวด")
        qr_label.setFont(QFont("Lotuss Smart HL", 22, QFont.Bold))
        qr_label.setStyleSheet("color: rgb(1, 187, 181);")
        qr_label.setAlignment(Qt.AlignCenter)

        self.logo_label_footer = QLabel()
        logo_pixmap = QPixmap(os.path.join(script_dir, u"../resources/LogoLotus 100x30.png"))
        self.logo_label_footer.setPixmap(logo_pixmap)
        self.logo_label_footer.setStyleSheet("background-color: transparent;")

        self.qr = QLabel()
        self.qr.setStyleSheet("background-color: transparent;")

        self.qr_image = self.lotus_system.getQR()
        qr_pixmap = QPixmap(os.path.join(script_dir, u"../resources/QRDemo.png"))
        self.qr.setPixmap(qr_pixmap)
        self.qr.setAlignment(Qt.AlignCenter)

        qr_layout = QVBoxLayout()
        qr_layout.addWidget(qr_label)
        qr_layout.addSpacing(15)
        qr_layout.addWidget(self.qr)

        footer_layout = QHBoxLayout()
        footer_layout.addStretch(1)
        footer_layout.addWidget(self.logo_label_footer)

        qr_widget = QWidget()  # Create a widget to contain the layout
        qr_widget.setLayout(qr_layout)  # Set the layout to the widget
        qr_widget.setStyleSheet("background-color: white;")  # Set the background color of the widget

        info_label = QLabel("ได้รับขวด")
        info_label.setFont(QFont("Lotuss Smart HL", 22))
        info_label.setStyleSheet('''
                            QLabel {
                                color: rgb(0, 0, 0);
                                background-color: transparent;
                            }
                        ''')

        # self.count_label = QLabel(str(self.bottle_count))
        self.count_label = QLabel(str(self.lotus_system.bottle))
        self.count_label.setFont(QFont("Lotuss Smart HL", 30))
        self.count_label.setStyleSheet('''
                                    QLabel {
                                        color: rgb(0, 0, 0);
                                        background-color: transparent;
                                    }
                                ''')

        bottle_logo = QLabel()
        bottle_logo.setStyleSheet("background-color: transparent;")
        bottle_pixmap = QPixmap(os.path.join(script_dir, u"../resources/bottle.png")).scaled(25, 50)
        bottle_logo.setPixmap(bottle_pixmap)

        done_button = QPushButton("เสร็จสิ้น")
        done_button.setFont(QFont("Lotuss Smart HL", 20, QFont.Bold))
        done_button.setStyleSheet('''
                            QPushButton {
                                color: rgb(255, 255, 255);
                                background-color: rgb(255, 196, 0);
                                border-radius: 20px;
                                border: none; /* Ensure no border */
                                padding: 5px; /* Adjust padding */
                            }
                        ''')
        done_button.clicked.connect(self.reset)

        value_layout = QHBoxLayout()
        value_layout.addStretch(1)
        value_layout.addWidget(info_label)
        value_layout.addSpacing(5)
        value_layout.addWidget(self.count_label)
        value_layout.addSpacing(5)
        value_layout.addWidget(bottle_logo)
        value_layout.addStretch(1)

        right_layout = QVBoxLayout()
        right_layout.addSpacing(30)
        right_layout.addLayout(value_layout)
        right_layout.addStretch(1)
        right_layout.addWidget(done_button)

        leftright_layout = QHBoxLayout()
        # leftright_layout.addSpacing(45)
        leftright_layout.addStretch(1)
        leftright_layout.addWidget(qr_widget)
        leftright_layout.addStretch(1)
        # leftright_layout.addSpacing(40)
        leftright_layout.addLayout(right_layout)
        leftright_layout.addStretch(1)
        # leftright_layout.addStretch(40)

        main_layout = QVBoxLayout(self)
        main_layout.addSpacing(45)
        main_layout.addLayout(leftright_layout)
        main_layout.addStretch(1)
        main_layout.addLayout(footer_layout)

        # Set window title and geometry
        self.setWindowTitle("Done Page")
        self.setStyleSheet("background-color: white;")
        self.setFixedSize(640, 480)
        self.update_background()
        self.show()

    def update_background(self):
        # Scale the background image to fit the current size of the widget
        self.background_pixmap = self.background_pixmap.scaled(self.width(), self.height() - (self.height() / 7))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.background_pixmap)

    def reset(self):
        self.lotus_system.setPage("StartPage")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = DonePage()
    sys.exit(app.exec())
