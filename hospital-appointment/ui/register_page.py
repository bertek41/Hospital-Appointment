from datetime import datetime

from PyQt5 import QtWidgets, QtGui, uic, QtCore
from PyQt5.QtCore import Qt
from ui.ui_utils import err, info
from models import User
from utils import pass_hash, icon, absolute_asset_path
from id_check import check_civil


class RegisterPage(QtWidgets.QDialog):
    pushButton: QtWidgets.QPushButton
    tc: QtWidgets.QLineEdit
    password: QtWidgets.QLineEdit
    passwordAgain: QtWidgets.QLineEdit
    name: QtWidgets.QLineEdit
    surname: QtWidgets.QLineEdit
    dateEdit: QtWidgets.QDateEdit

    def __init__(self, parent: QtWidgets.QWidget):
        super().__init__()
        self.parent = parent
        uic.loadUi(
            absolute_asset_path("ui/register.ui"),
            self,
        )
        self.setWindowIcon(icon)
        self.setFixedSize(304, 255)
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        self.pushButton.clicked.connect(self.clicked)

        rx = QtCore.QRegExp("[0-9]{11}")
        val = QtGui.QRegExpValidator(rx)
        self.tc.setValidator(val)
        self.password.setMaxLength(32)
        self.passwordAgain.setMaxLength(32)
        self.name.setMaxLength(41)
        self.surname.setMaxLength(41)
        self.dateEdit.setDate(datetime.today())
        self.show()
        self.closeEvent = self.closed

    def closed(self, event):
        self.parent.show()
        event.accept()

    def clicked(self):

        self.pushButton.setEnabled(False)

        tcText = self.tc.text()
        if (
            not tcText
            or not self.password.text()
            or not self.passwordAgain.text()
            or not self.name.text()
            or not self.surname.text()
        ):
            err("Tüm alanları doldurunuz.")
        elif len(tcText) != 11:
            err("TC Kimlik Numaranız 11 haneli olmalıdır")
        elif len(self.password.text()) < 6:
            err("Şifreniz en az 6 karakter olmalıdır")
        elif User.objects(tc=tcText).first():
            err("Bu TC Kimlik Numarası zaten kayıtlı")
        elif self.password.text() != self.passwordAgain.text():
            err("Şifreler uyuşmuyor")
        elif not check_civil(
            tcText,
            self.name.text(),
            self.surname.text(),
            int(self.dateEdit.date().toPyDate().year),
        ):
            err("Böyle bir vatandaş bulunamadı")
        else:
            User(
                tc=tcText,
                password=pass_hash(self.password.text()),
                name=self.name.text(),
                surname=self.surname.text(),
                birth_date=self.dateEdit.date().toPyDate(),
            ).save()
            info(text="Kayıt başarılı, lütfen giriş yapın")
            self.hide()
            self.parent.show()
        self.pushButton.setEnabled(True)
