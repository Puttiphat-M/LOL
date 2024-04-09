import os
from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout
from PySide6.QtGui import QPixmap, QPainter, QFont


def go_to_donate_page():
    from System.LotusSystem import LotusSystem
    LotusSystem.set_page("DonatePage")


def go_to_done_page():
    from System.LotusSystem import LotusSystem
    LotusSystem.set_page("DonePage")


class DepositPage(QWidget):
    def __init__(self):
        super().__init__()
        script_dir = os.path.dirname(os.path.abspath(__file__))

        info_label = QLabel("หากท่านมี 10 ขวด จะสามารถแลกไข่ได้ 1 ฟอง")
        info_label.setFont(QFont("Lotuss Smart HL", 22, QFont.Light))
        info_label.setStyleSheet('''
                            QLabel {
                                color: rgb(0, 0, 0);
                                background-color: transparent;
                            }
                        ''')
        info_label.setAlignment(Qt.AlignCenter)

        X_symbol = QLabel("x")
        X_symbol.setFont(QFont("Lotuss Smart HL", 45, QFont.Medium))
        X_symbol.setStyleSheet('''
                            QLabel {
                                color: rgb(0, 0, 0);
                                background-color: transparent;
                            }
                        ''')

        from System.LotusSystem import LotusSystem
        self.count_label = QLabel(str(LotusSystem.get_bottle_count()))
        self.count_label.setFont(QFont("Lotuss Smart HL", 70))
        self.count_label.setStyleSheet('''
                                    QLabel {
                                        color: rgb(0, 0, 0);
                                        background-color: transparent;
                                    }
                                ''')

        bottle_logo = QLabel()
        bottle_logo.setStyleSheet("background-color: transparent;")
        bottle_pixmap = QPixmap(os.path.join(script_dir, u"../resources/bottle.png"))
        bottle_logo.setPixmap(bottle_pixmap)

        value_layout = QHBoxLayout()
        value_layout.addStretch(1)
        value_layout.addWidget(X_symbol)
        value_layout.addSpacing(10)
        value_layout.addWidget(self.count_label)
        value_layout.addSpacing(10)
        value_layout.addWidget(bottle_logo)
        value_layout.addStretch(1)

        limit_label = QLabel("สูงสุด 10 ขวดต่อวัน")
        limit_label.setFont(QFont("Lotuss Smart HL", 22, QFont.Light))
        limit_label.setStyleSheet('''
                                    QLabel {
                                        color: rgb(0, 0, 0);
                                        background-color: transparent;
                                    }
                                ''')
        limit_label.setAlignment(Qt.AlignCenter)

        notice = QLabel("กรุณาหยอดขวด")
        notice.setFont(QFont("Lotuss Smart HL", 30, QFont.Medium))
        notice.setStyleSheet('''
                            QLabel {
                                color: rgb(216, 7, 5);
                                background-color: transparent;
                            }
                        ''')
        notice.setAlignment(Qt.AlignCenter)

        self.notice_layout = QHBoxLayout()
        self.notice_layout.addWidget(notice)

        self.logo_label_footer = QLabel()
        logo_pixmap = QPixmap(os.path.join(script_dir, u"../resources/LogoLotus 100x30.png"))
        self.logo_label_footer.setPixmap(logo_pixmap)
        self.logo_label_footer.setStyleSheet("background-color: transparent;")

        footer_layout = QHBoxLayout()
        footer_layout.addStretch(1)
        footer_layout.addWidget(self.logo_label_footer)

        main_layout = QVBoxLayout(self)
        main_layout.addStretch(1)
        main_layout.addWidget(info_label)
        main_layout.addStretch(1)
        main_layout.addLayout(value_layout)
        main_layout.addStretch(1)
        main_layout.addWidget(limit_label)
        main_layout.addStretch(1)
        main_layout.addLayout(self.notice_layout)
        main_layout.addStretch(1)
        main_layout.addLayout(footer_layout)

        LotusSystem.get_instance().bottle_changed.connect(self.increase_bottle_count)

        self.setWindowTitle("Deposit Page")
        self.setStyleSheet("background-color: white;")
        self.setFixedSize(640, 480)
        self.show()

    @Slot(int)
    def increase_bottle_count(self):
        from System.LotusSystem import LotusSystem
        self.count_label.setText(str(LotusSystem.get_bottle_count()))
        if self.notice_layout.count() == 1:
            while self.notice_layout.count() > 0:
                item = self.notice_layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()
            self.update_button_state()

    def update_button_state(self):
        collect_button = QPushButton("สะสมขวด")
        collect_button.setFont(QFont("Lotuss Smart HL", 22, QFont.Bold))
        collect_button.setFixedSize(230, 52)
        collect_button.setStyleSheet('''
                    QPushButton {
                        color: rgb(255, 255, 255);
                        background-color: rgb(255, 196, 0);
                        border-radius: 25px;
                    }
                ''')
        collect_button.clicked.connect(go_to_done_page)

        donate_button = QPushButton("บริจาค")
        donate_button.setFont(QFont("Lotuss Smart HL", 22, QFont.Bold))
        donate_button.setFixedSize(230, 52)
        donate_button.setStyleSheet('''
                            QPushButton {
                                color: rgb(255, 255, 255);
                                background-color: rgb(255, 196, 0);
                                border-radius: 25px;
                            }
                        ''')
        donate_button.clicked.connect(go_to_donate_page)

        self.notice_layout.addStretch(1)
        self.notice_layout.addWidget(collect_button)
        self.notice_layout.addStretch(1)
        self.notice_layout.addWidget(donate_button)
        self.notice_layout.addStretch(1)

    def paintEvent(self, event):
        painter = QPainter(self)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        painter.drawPixmap(0, 0, QPixmap(os.path.join(script_dir, u"../resources/LotusBackground.jpg")).scaled(self.width(), self.height() - (self.height() / 7)))
