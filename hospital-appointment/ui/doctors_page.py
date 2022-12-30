from datetime import datetime

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from .ui_utils import err, info, yesno
from ui.table_model import TableModel
from ui.appointment_dates import AppointmentDates
from ui.add_doctor_page import AddDoctor
from ui.add_appointment_date_page import AddAppointmentDate
from ui.appointments_of_doctor import AppointmentsOfDoctor
from models import Doctor, User
from utils import icon


class DoctorsPage(QtWidgets.QMainWindow):
    tableView: QtWidgets.QTableView
    actionEkle: QtWidgets.QAction
    actionDuzenle: QtWidgets.QAction
    actionRandevu_Tarihi_Ekle: QtWidgets.QAction
    actionViewAppointments: QtWidgets.QAction
    actionSil: QtWidgets.QAction
    need_update = False

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.resize(560, 360)
        self.centralwidget = QtWidgets.QWidget(self)
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setGeometry(QtCore.QRect(0, 0, 562, 341))
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 560, 21))
        self.menuDoktor = QtWidgets.QMenu(self.menubar)
        self.setMenuBar(self.menubar)
        self.actionEkle = QtWidgets.QAction(self)
        self.actionDuzenle = QtWidgets.QAction(self)
        self.actionSil = QtWidgets.QAction(self)
        self.actionRandevu_Tarihi_Ekle = QtWidgets.QAction(self)
        self.actionRandevu_Tarihlerini_Goruntule = QtWidgets.QAction(self)
        self.actionViewAppointments = QtWidgets.QAction(self)
        self.menuDoktor.addAction(self.actionEkle)
        self.menuDoktor.addSeparator()
        self.menuDoktor.addAction(self.actionDuzenle)
        self.menuDoktor.addAction(self.actionRandevu_Tarihi_Ekle)
        self.menuDoktor.addAction(self.actionRandevu_Tarihlerini_Goruntule)
        self.menuDoktor.addAction(self.actionViewAppointments)
        self.menuDoktor.addAction(self.actionSil)
        self.menubar.addAction(self.menuDoktor.menuAction())

        self.setWindowTitle("Doktorlar")
        self.menuDoktor.setTitle("Doktor")
        self.actionEkle.setText("Ekle")
        self.actionEkle.setShortcut("Ctrl+E")
        self.actionDuzenle.setText("Düzenle")
        self.actionDuzenle.setShortcut("Ctrl+D")
        self.actionSil.setText("Sil")
        self.actionSil.setShortcut("Ctrl+S")
        self.actionRandevu_Tarihi_Ekle.setText("Randevu Tarihi Ekle")
        self.actionRandevu_Tarihi_Ekle.setShortcut("Ctrl+T")
        self.actionRandevu_Tarihlerini_Goruntule.setText(
            "Randevu Tarihlerini Görüntüle"
        )
        self.actionRandevu_Tarihlerini_Goruntule.setShortcut("Ctrl+G")
        self.actionViewAppointments.setText("Randevuları Görüntüle")
        self.actionViewAppointments.setShortcut("Ctrl+R")

        self.setWindowIcon(icon)
        self.setFixedSize(562, 362)
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        self.closeEvent = self.closed
        self.update_table()

        self.actionEkle.triggered.connect(self.add_doctor)
        self.actionDuzenle.triggered.connect(self.edit_doctor)
        self.actionRandevu_Tarihi_Ekle.triggered.connect(self.add_appointment_date)
        self.actionRandevu_Tarihlerini_Goruntule.triggered.connect(
            self.show_appointment_dates
        )
        self.actionViewAppointments.triggered.connect(self.view_appointments)
        self.actionSil.triggered.connect(self.delete_doctor)
        QtCore.QMetaObject.connectSlotsByName(self)

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
        for doctor in Doctor.objects:
            data.append(
                [
                    doctor.id,
                    doctor.name,
                    doctor.city,
                    doctor.county,
                    doctor.clinic,
                    doctor.hospital,
                ]
            )
        self.model = TableModel(
            data, ["Id", "Ad", "Şehir", "İlçe", "Klinik", "Hastane"]
        )
        self.tableView.setModel(self.model)
        self.tableView.setColumnHidden(0, True)
        self.tableView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableView.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.tableView.mouseDoubleClickEvent = self.edit_doctor

    def show(self):
        super().show()
        print("show")
        if self.need_update:
            self.update_table()
            self.need_update = False

    def closed(self, event):
        self.parent.show()
        event.accept()

    def add_doctor(self):
        print("add doctor")
        self.add = AddDoctor(self)
        self.hide()

    def read_doctor(self):
        if self.tableView.selectionModel().hasSelection():
            index = self.tableView.selectionModel().selectedRows()[0]
            doctor_id = self.model.data(index.siblingAtColumn(0))
            return Doctor.objects(id=doctor_id).first()

    def edit_doctor(self, event=None):
        print("edit doctor")
        doctor = self.read_doctor()
        if doctor:
            self.add = AddDoctor(self, doctor)
            self.hide()
        else:
            err("Lütfen bir doktor seçiniz.")

    def add_appointment_date(self):
        print("add appointment date")
        doctor = self.read_doctor()
        if doctor:
            self.add = AddAppointmentDate(self, doctor)
            self.hide()
        else:
            err("Lütfen bir doktor seçiniz.")

    def show_appointment_dates(self):
        print("show appointment dates")
        doctor = self.read_doctor()
        if doctor:
            self.appointment_dates = AppointmentDates(self, doctor)
            self.hide()
        else:
            err("Lütfen bir doktor seçiniz.")

    def view_appointments(self):
        print("view appointments")
        doctor = self.read_doctor()
        if doctor:
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
                self.appointments = AppointmentsOfDoctor(self, doctor)
                self.hide()
            else:
                err("Doktorun randevusu bulunmamaktadır.")
        else:
            err("Lütfen bir doktor seçiniz.")

    def delete_doctor(self):
        print("delete doctor")
        doctor = self.read_doctor()
        if doctor:
            if not yesno(text="Doktoru silmek istediğinize emin misiniz?"):
                return
            doctor.delete()
            info(text="Doktor başarıyla silindi")
            if len(Doctor.objects) == 0:
                self.close()
            else:
                index = self.tableView.currentIndex()
                self.update_table()
                if self.tableView.model().rowCount(None) <= index.row():
                    self.tableView.selectRow(index.row() - 1)
                else:
                    self.tableView.selectRow(index.row())
        else:
            err("Lütfen bir doktor seçiniz.")
