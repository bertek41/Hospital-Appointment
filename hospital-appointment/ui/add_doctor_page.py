from PyQt5 import QtWidgets, QtGui, uic
from PyQt5.QtCore import Qt
from ui.ui_utils import err, info
from utils import absolute_asset_path, icon
from models import Doctor


class AddDoctor(QtWidgets.QDialog):
    name: QtWidgets.QLineEdit
    clinic: QtWidgets.QLineEdit
    city: QtWidgets.QLineEdit
    county: QtWidgets.QLineEdit
    hospital: QtWidgets.QPlainTextEdit
    pushButton: QtWidgets.QPushButton

    def __init__(self, parent, doctor=None):
        super().__init__()
        self.parent = parent
        self.doctor = doctor
        uic.loadUi(
            absolute_asset_path("ui/add_doctor.ui"),
            self,
        )
        if doctor:
            self.setWindowTitle("Doktor Düzenle")
            self.pushButton.setText("Düzenle")
            self.pushButton.clicked.connect(self.edit_doctor)

            self.name.setText(doctor.name)
            self.clinic.setText(doctor.clinic)
            self.city.setText(doctor.city)
            self.county.setText(doctor.county)
            self.hospital.setPlainText(doctor.hospital)
        else:
            self.pushButton.clicked.connect(self.add_doctor)
        self.name.setMaxLength(81)
        self.clinic.setMaxLength(41)
        self.city.setMaxLength(41)
        self.county.setMaxLength(41)
        self.hospital.textChanged.connect(self.check_text)
        self.setWindowIcon(icon)
        self.setFixedSize(336, 310)
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        self.show()
        self.closeEvent = self.closed

    def closed(self, event):
        self.parent.show()
        event.accept()

    def check_text(self):
        self.pushButton.setEnabled(False)
        text = self.hospital.toPlainText()
        if len(text) > 100:
            self.hospital.setPlainText(text[:100])
            self.hospital.moveCursor(QtGui.QTextCursor.End)
        self.pushButton.setEnabled(True)

    def add_doctor(self):
        print("add doctor")
        if (
            not self.name.text()
            or not self.clinic.text()
            or not self.city.text()
            or not self.county.text()
            or not self.hospital.toPlainText()
        ):
            err("Lütfen tüm alanları doldurunuz!")
            return
        Doctor(
            name=self.name.text(),
            clinic=self.clinic.text(),
            city=self.city.text(),
            county=self.county.text(),
            hospital=self.hospital.toPlainText(),
        ).save()
        info(text="Doktor başarıyla eklendi!")
        self.parent.need_update = True
        self.close()

    def edit_doctor(self):
        print("edit doctor")
        if (
            not self.name.text()
            or not self.clinic.text()
            or not self.city.text()
            or not self.county.text()
            or not self.hospital.toPlainText()
        ):
            err("Lütfen tüm alanları doldurunuz!")
            return
        self.doctor.name = self.name.text()
        self.doctor.clinic = self.clinic.text()
        self.doctor.city = self.city.text()
        self.doctor.county = self.county.text()
        self.doctor.hospital = self.hospital.toPlainText()
        self.doctor.save()
        info(text="Doktor başarıyla düzenlendi!")
        self.parent.need_update = True
        self.close()
