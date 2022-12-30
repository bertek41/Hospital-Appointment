from datetime import datetime

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt
from ui.ui_utils import err, info, yesno
from ui.table_model import TableModel
from ui.select_doctor_date import SelectDoctorDate
from models import Doctor, User
from utils import absolute_asset_path, icon


class AppointmentsOfDoctor(QtWidgets.QMainWindow):
    tableView: QtWidgets.QTableView
    actionCancel: QtWidgets.QAction

    def __init__(self, parent, doctor):
        super().__init__()
        self.parent = parent
        self.doctor = doctor
        uic.loadUi(
            absolute_asset_path("ui/appointments_of_doctor.ui"),
            self,
        )
        self.setWindowIcon(icon)
        self.setFixedSize(560, 360)
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        self.actionCancel.triggered.connect(self.cancel)
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
        for user in User.objects():
            for appointment in user.appointments:
                if appointment.date.date() < datetime.today().date():
                    continue
                if appointment.doctor.id == self.doctor.id:
                    data.append(
                        [
                            user.id,
                            user.name + " " + user.surname,
                            appointment.doctor.name,
                            appointment.doctor.clinic,
                            appointment.doctor.city,
                            appointment.doctor.county,
                            appointment.doctor.hospital,
                            appointment.date.strftime("%d.%m.%Y %H:%M"),
                        ]
                    )
        self.model = TableModel(
            data, ["Id", "Ad", "Doktor", "Klinik", "Şehir", "İlçe", "Hastane", "Tarih"]
        )
        self.tableView.setModel(self.model)
        self.tableView.setColumnHidden(0, True)
        self.tableView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableView.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.tableView.mouseDoubleClickEvent = self.cancel

    def closed(self, event):
        self.parent.show()
        event.accept()

    def read_user_and_date(self):
        if self.tableView.selectionModel().hasSelection():
            index = self.tableView.selectionModel().selectedRows()[0]
            user_id = self.model.data(index.siblingAtColumn(0))
            date = self.model.data(index.siblingAtColumn(7))
            return User.objects(id=user_id).first(), datetime.strptime(
                date, "%d.%m.%Y %H:%M"
            )

    def cancel(self, event=None):
        user_and_date = self.read_user_and_date()
        if user_and_date is None:
            err("Lütfen bir hasta seçiniz.")
            return
        if yesno("Randevuyu iptal etmek istediğinize emin misiniz?"):
            user, date = user_and_date
            if user:
                for appointment in user.appointments:
                    if appointment.date == date:
                        appointment.doctor.appointment_dates.filter(
                            date=appointment.date
                        ).first().is_available = True
                        appointment.doctor.save()
                        user.appointments.remove(appointment)
                        user.save()
                        info("Randevu iptal edildi")
                        found = False
                        for user in User.objects():
                            for appointment in user.appointments:
                                if (
                                    appointment.doctor.id == doctor.id
                                    and appointment.date >= datetime.now()
                                ):
                                    found = True
                                    break
                        if found:
                            self.update_table()
                        else:
                            self.close()
