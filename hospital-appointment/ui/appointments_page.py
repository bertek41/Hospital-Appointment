from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt
from ui.ui_utils import err, info, yesno
from ui.table_model import TableModel
from utils import absolute_asset_path, icon
from datetime import datetime


class AppointmentsPage(QtWidgets.QMainWindow):
    actionCancel: QtWidgets.QAction
    tableView: QtWidgets.QTableView

    def __init__(self, parent, user):
        super().__init__()
        self.parent = parent
        self.user = user
        uic.loadUi(
            absolute_asset_path("ui/appointments.ui"),
            self,
        )
        self.setWindowIcon(icon)
        self.setFixedSize(560, 360)
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        self.update_table()
        self.actionCancel.triggered.connect(self.cancel)
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
        for appointment in self.user.appointments:
            data.append(
                [
                    appointment.id,
                    appointment.doctor.name,
                    appointment.doctor.clinic,
                    appointment.doctor.city,
                    appointment.doctor.county,
                    appointment.doctor.hospital,
                    datetime.strftime(appointment.date, "%d.%m.%Y %H:%M"),
                ]
            )
        self.model = TableModel(
            data, ["Id", "Doktor Adı", "Klinik", "Şehir", "İlçe", "Hastane", "Tarih"]
        )
        self.tableView.setModel(self.model)
        self.tableView.setColumnHidden(0, True)
        self.tableView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableView.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.tableView.mouseDoubleClickEvent = self.cancel

    def closed(self, event):
        self.parent.show()
        event.accept()

    def cancel(self, event=None):
        print("cancel")
        if self.tableView.selectionModel().hasSelection():
            index = self.tableView.selectionModel().selectedRows()[0]
            appointment_id = self.model.data(index.siblingAtColumn(0))
            appointment = self.user.appointments.filter(id=appointment_id).first()
            if appointment.date > datetime.now():
                if not yesno(text="Randevunuzu iptal etmek istediğinize emin misiniz?"):
                    return
                self.user.appointments.remove(appointment)
                self.user.save()
                appointment.doctor.appointment_dates.filter(
                    date=appointment.date
                ).first().is_available = True
                appointment.doctor.save()
                info(text="Randevunuz iptal edildi.")
                if len(self.user.appointments) == 0:
                    self.close()
                else:
                    self.update_table()
            else:
                err("Randevunuzun tarihi geçmiş.")
