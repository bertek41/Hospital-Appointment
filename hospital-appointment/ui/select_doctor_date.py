from PyQt5 import QtWidgets, QtGui, uic
from PyQt5.QtCore import Qt
from ui.ui_utils import LazyPage, err, info
from models import Appointment
from utils import absolute_asset_path, icon


class SelectDoctorDate(QtWidgets.QDialog):
    listView: QtWidgets.QListView
    selectButton: QtWidgets.QPushButton

    def __init__(self, parent, user, doctor, appointment_dates):
        super().__init__()
        self.parent = parent
        self.user = user
        self.doctor = doctor
        self.appointment_dates = appointment_dates
        uic.loadUi(
            absolute_asset_path("ui/appointment_doctor_times.ui"),
            self,
        )
        self.setWindowIcon(icon)
        self.setFixedSize(201, 280)
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        self.update_table()
        self.selectButton.clicked.connect(self.select)

        self.closeEvent = self.closed
        self.show()

    def update_table(self):
        model = QtGui.QStandardItemModel()
        self.listView.setModel(model)
        self.listView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.listView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        for date in self.appointment_dates:
            item = QtGui.QStandardItem(date.date.strftime("%d.%m.%Y %H:%M"))
            item.setTextAlignment(Qt.AlignCenter)
            model.appendRow(item)

    def closed(self, event):
        self.parent.show()
        event.accept()

    def select(self):
        if self.listView.selectionModel().hasSelection():
            index = self.listView.selectionModel().selectedRows()[0]
            date = self.appointment_dates[index.row()]
            date.is_available = False
            self.user.appointments.append(
                Appointment(doctor=self.doctor, date=date.date)
            )
            self.doctor.save()
            self.user.save()
            info(
                f"{self.doctor.name} isimli doktora "
                f"{date.date.strftime('%d.%m.%Y %H:%M')} "
                f"tarihinde {self.doctor.clinic} kliniğine randevu alındı."
            )
            self.accept()
            self.parent = LazyPage("MainPage", self.user)
        else:
            err("Lütfen bir tarih seçiniz.")
