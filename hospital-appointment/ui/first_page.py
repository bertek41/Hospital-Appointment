from PyQt5 import QtWidgets, QtGui, uic
from PyQt5.QtCore import Qt
from ui.ui_utils import LazyPage
from utils import absolute_asset_path, icon


class FirstPage(QtWidgets.QDialog):
    pushButton: QtWidgets.QPushButton
    pushButton_2: QtWidgets.QPushButton

    def __init__(self):
        super().__init__()
        uic.loadUi(
            absolute_asset_path("ui/first_page.ui"),
            self,
        )
        self.setWindowIcon(icon)
        self.setFixedSize(360, 150)
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        self.pushButton.clicked.connect(self.login)
        self.pushButton_2.clicked.connect(self.register)
        self.show()

    def register(self):
        self.hide()
        self.register_page = LazyPage("RegisterPage", self)

    def login(self):
        self.hide()
        self.login_page = LazyPage("LoginPage", self)
