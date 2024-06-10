from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QApplication
from PySide6.QtGui import QPixmap, QFont, QPainter


class DepositPage(QWidget):
    def __init__(self):
        super().__init__()
        self.set_full_screen()

        self.info_label = QLabel("หากท่านมี 10 ขวด จะสามารถแลกไข่ได้ 1 ฟอง")
        self.info_label.setFont(QFont("Lotuss Smart HL", 22, QFont.Light))
        self.info_label.setStyleSheet('''
                            QLabel {
                                color: rgb(0, 0, 0);
                                background-color: transparent;
                            }
                        ''')
        self.info_label.setAlignment(Qt.AlignCenter)

        self.x_symbol = QLabel("x")
        self.x_symbol.setFont(QFont("Lotuss Smart HL", 45, QFont.Medium))
        self.x_symbol.setStyleSheet('''
                            QLabel {
                                color: rgb(0, 0, 0);
                                background-color: transparent;
                            }
                        ''')

        from LotusSystem import LotusSystem
        self.count_label = QLabel(str(LotusSystem.get_bottle_count()))
        self.count_label.setFont(QFont("Lotuss Smart HL", 70))
        self.count_label.setStyleSheet('''
                                    QLabel {
                                        color: rgb(0, 0, 0);
                                        background-color: transparent;
                                    }
                                ''')

        self.bottle_logo = QLabel()
        self.bottle_logo.setStyleSheet("background-color: transparent;")
        from UI.Component import resource_path
        self.bottle_pixmap = QPixmap(resource_path("resources/bottle.png"))
        self.bottle_logo.setPixmap(self.bottle_pixmap)
        self.bottle_logo.setAlignment(Qt.AlignCenter)

        value_layout = QHBoxLayout()
        value_layout.addStretch(1)
        value_layout.addWidget(self.x_symbol)
        value_layout.addSpacing(8)
        value_layout.addWidget(self.count_label)
        value_layout.addSpacing(8)
        value_layout.addWidget(self.bottle_logo)
        value_layout.addStretch(1)

        self.limit_label = QLabel("สูงสุด 10 ขวดต่อวัน")
        self.limit_label.setFont(QFont("Lotuss Smart HL", 22, QFont.Light))
        self.limit_label.setStyleSheet('''
                                    QLabel {
                                        color: rgb(0, 0, 0);
                                        background-color: transparent;
                                    }
                                ''')
        self.limit_label.setAlignment(Qt.AlignCenter)

        self.notice = QLabel("กรุณาหยอดขวด")
        self.notice.setFont(QFont("Lotuss Smart HL", 30, QFont.Medium))
        self.notice.setStyleSheet('''
                            QLabel {
                                color: rgb(216, 7, 5);
                                background-color: transparent;
                            }
                        ''')
        self.notice.setAlignment(Qt.AlignCenter)

        self.notice_layout = QHBoxLayout()
        self.notice_layout.addWidget(self.notice)

        self.logo_label_footer = QLabel()
        self.logo_pixmap = QPixmap(resource_path("resources/Lotus.png"))
        self.logo_label_footer.setPixmap(self.logo_pixmap)
        self.logo_label_footer.setStyleSheet("background-color: transparent;")

        footer_layout = QHBoxLayout()
        footer_layout.addStretch(1)
        footer_layout.addWidget(self.logo_label_footer)

        self.footer_container = QWidget()
        self.footer_container.setLayout(footer_layout)
        self.footer_container.setStyleSheet("background-color: white;")

        main_layout = QVBoxLayout(self)
        main_layout.addStretch(1)
        main_layout.addWidget(self.info_label)
        main_layout.addStretch(1)
        main_layout.addLayout(value_layout)
        main_layout.addStretch(1)
        main_layout.addWidget(self.limit_label)
        main_layout.addStretch(1)
        main_layout.addLayout(self.notice_layout)
        main_layout.addStretch(1)
        main_layout.addWidget(self.footer_container)
        main_layout.setContentsMargins(0, 0, 0, 0)

        LotusSystem.get_instance().bottle_changed.connect(self.increase_bottle_count)

        self.setWindowTitle("Deposit Page")
        self.setStyleSheet("background-color: white;")
        self.setMinimumSize(640, 500)
        self.show()

    @Slot(int)
    def increase_bottle_count(self):
        from LotusSystem import LotusSystem
        self.count_label.setText(str(LotusSystem.get_bottle_count()))
        if self.notice_layout.count() == 1:
            while self.notice_layout.count() > 0:
                item = self.notice_layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()
            self.update_button_state()

    def update_button_state(self):
        self.collect_button = QPushButton("สะสมขวด")
        self.collect_button.setFont(QFont("Lotuss Smart HL", int((self.width() + self.height()) / 55), QFont.Bold))

        self.collect_button.setFixedSize(int(self.width() * 0.2), int(self.height() * 0.08))
        self.collect_button.setStyleSheet('''
                    QPushButton {
                        color: rgb(255, 255, 255);
                        background-color: rgb(255, 196, 0);
                        border-radius: 25px;
                    }
                ''')
        self.collect_button.clicked.connect(self.go_to_done_page)

        self.donate_button = QPushButton("บริจาค")
        self.donate_button.setFont(QFont("Lotuss Smart HL", int((self.width() + self.height()) / 55), QFont.Bold))
        self.donate_button.setFixedSize(int(self.width() * 0.2), int(self.height() * 0.08))
        self.donate_button.setStyleSheet('''
                            QPushButton {
                                color: rgb(255, 255, 255);
                                background-color: rgb(255, 196, 0);
                                border-radius: 25px;
                            }
                        ''')
        self.donate_button.clicked.connect(self.go_to_donate_page)

        self.notice_layout.addStretch(1)
        self.notice_layout.addWidget(self.collect_button)
        self.notice_layout.addStretch(1)
        self.notice_layout.addWidget(self.donate_button)
        self.notice_layout.addStretch(1)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.updateUI()

    def updateUI(self):
        width_ratio = self.width() / 640
        height_ratio = self.height() / 480
        button_width = int(self.width() * 0.2)
        button_height = int(self.height() * 0.08)
        x_size = int(45 * (width_ratio + height_ratio) / 2)
        amount_size = int(75 * (width_ratio + height_ratio) / 2)
        bottle_size = int(60 * (width_ratio + height_ratio) / 2)
        self.x_symbol.setFont(QFont("Lotuss Smart HL", x_size, QFont.Medium))
        self.count_label.setFont(QFont("Lotuss Smart HL", amount_size))
        self.bottle_logo.setPixmap(self.bottle_pixmap.scaled(bottle_size, bottle_size, Qt.KeepAspectRatio))
        self.info_label.setFont(QFont("Lotuss Smart HL", int((self.width() + self.height()) / 55)))
        self.limit_label.setFont(QFont("Lotuss Smart HL", int((self.width() + self.height()) / 55)))
        self.logo_label_footer.setPixmap(self.logo_pixmap.scaled(self.width() / 6.4, self.height() / 15, Qt.KeepAspectRatio))
        if self.notice_layout.count() == 1:
            self.notice.setFont(QFont("Lotuss Smart HL", int((self.width() + self.height()) / 45), QFont.Medium))
        if hasattr(self, 'donate_button'):
            self.donate_button.setFont(QFont("Lotuss Smart HL", int((self.width() + self.height()) / 55), QFont.Bold))
            self.donate_button.setFixedSize(button_width, button_height)
        if hasattr(self, 'collect_button'):
            self.collect_button.setFont(QFont("Lotuss Smart HL", int((self.width() + self.height()) / 55), QFont.Bold))
            self.collect_button.setFixedSize(button_width, button_height)

    def set_full_screen(self):
        screen_geometry = QApplication.primaryScreen().geometry()
        self.setGeometry(screen_geometry)

    def paintEvent(self, event):
        from UI.Component import resource_path
        painter = QPainter(self)
        painter.drawPixmap(0, 0, QPixmap(resource_path("resources/LotusBackground.jpg")).scaled(self.width(), self.height()))
        painter.end()

    def go_to_donate_page(self):
        from LotusSystem import LotusSystem
        LotusSystem.set_page("DonatePage")
        self.close()

    def go_to_done_page(self):
        from LotusSystem import LotusSystem
        LotusSystem.set_page("DonePage")
        self.close()
