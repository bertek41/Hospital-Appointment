from PyQt5 import QtWidgets, QtCore, QtGui, uic
from PyQt5.QtCore import Qt
from ui.ui_utils import err
from models import User
from ui.main_page import MainPage
from utils import pass_hash, absolute_asset_path, icon


class LoginPage(QtWidgets.QDialog):
    pushButton: QtWidgets.QPushButton
    tc: QtWidgets.QLineEdit
    password: QtWidgets.QLineEdit

    def __init__(self, parent: QtWidgets.QWidget = None):
        super().__init__()
        self.parent = parent
        uic.loadUi(
            absolute_asset_path("ui/login.ui"),
            self,
        )
        self.setWindowIcon(icon)
        self.setFixedSize(334, 233)
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        self.pushButton.clicked.connect(self.clicked)
        rx = QtCore.QRegExp("[0-9]{11}")
        val = QtGui.QRegExpValidator(rx)
        self.tc.setValidator(val)
        self.password.setMaxLength(32)
        self.show()
        self.closeEvent = self.closed

    def closed(self, event):
        self.parent.show()
        event.accept()

    def clicked(self):
        self.pushButton.setEnabled(False)

        if not self.tc.text() or not self.password.text():
            err("TC Kimlik Numarası ve Şifre boş bırakılamaz")
        self.user = User.objects(tc=self.tc.text()).first()
        if not self.user:
            err("Bu TC Kimlik Numarası kayıtlı değil")
        elif self.user.password != pass_hash(self.password.text()):
            err("Şifre yanlış")
        else:
            self.accept()
            self.main = MainPage(self.user)

        self.pushButton.setEnabled(True)
