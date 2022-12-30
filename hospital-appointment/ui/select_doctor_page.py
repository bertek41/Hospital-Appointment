from datetime import datetime

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt
from ui.ui_utils import err
from ui.table_model import TableModel
from ui.select_doctor_date import SelectDoctorDate
from models import Doctor
from utils import absolute_asset_path, icon


class SelectDoctor(QtWidgets.QMainWindow):
    tableView: QtWidgets.QTableView
    actionAl: QtWidgets.QAction

    def __init__(self, parent, user, doctors, startDate, endDate):
        super().__init__()
        self.parent = parent
        self.user = user
        self.doctors = doctors
        self.startDate = startDate
        self.endDate = endDate
        uic.loadUi(
            absolute_asset_path("ui/appointment_doctor_select.ui"),
            self,
        )
        self.setWindowIcon(icon)
        self.setFixedSize(560, 360)
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        self.actionAl.triggered.connect(self.get_appointment)
        self.update_table()

        self.closeEvent = self.closed
        self.show()

    def update_table(self):
        self.tableView.setSortingEnabled(True)
        self.tableView.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch
        )
        self.tableView.verticalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeToContents
        )
        data = []
        for doctor in self.doctors:
            data.append(
                [
                    doctor.id,
                    doctor.name,
                    doctor.clinic,
                    doctor.city,
                    doctor.county,
                    doctor.hospital,
                ]
            )
        self.model = TableModel(
            data, ["Id", "Ad", "Klinik", "Şehir", "İlçe", "Hastane"]
        )
        self.tableView.setModel(self.model)
        self.tableView.setColumnHidden(0, True)
        self.tableView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableView.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.tableView.mouseDoubleClickEvent = self.get_appointment

    def closed(self, event):
        self.parent.show()
        event.accept()

    def read_doctor(self):
        if self.tableView.selectionModel().hasSelection():
            index = self.tableView.selectionModel().selectedRows()[0]
            doctor_id = self.model.data(index.siblingAtColumn(0))
            return Doctor.objects(id=doctor_id).first()

    def get_appointment(self, event=None):
        doctor = self.read_doctor()
        if doctor:
            appointment_dates = doctor.available_appointments
            appointments = []
            closest_appointment = None
            for appointment_date in appointment_dates:
                if (
                    not closest_appointment
                    and appointment_date.date >= datetime.today()
                ) or (
                    datetime.today() <= appointment_date.date < closest_appointment.date
                ):
                    closest_appointment = appointment_date
                if self.startDate <= appointment_date.date.date() <= self.endDate:
                    appointments.append(appointment_date)
            if len(appointments) == 0:
                if closest_appointment:
                    err(
                        "Seçtiğiniz tarihler arasında randevu bulunmamaktadır."
                        "En yakın randevu tarihi {}".format(
                            closest_appointment.date.strftime("%d.%m.%Y")
                        )
                    )
                else:
                    err("Randevu bulunmamaktadır.")
                return
            self.select_doctor_date = SelectDoctorDate(
                self, self.user, doctor, appointments
            )
            self.hide()
        else:
            err("Lütfen bir doktor seçiniz.")
