from datetime import datetime

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt
from ui.ui_utils import err, info
from ui.appointment_dates_to_add_page import AppointmentDatesToAdd
from utils import next_workday, daterange, timerange, absolute_asset_path, icon
from models import AppointmentDate


class AddAppointmentDate(QtWidgets.QDialog):
    workDateStart: QtWidgets.QDateEdit
    workDateEnd: QtWidgets.QDateEdit
    workTimeStart: QtWidgets.QTimeEdit
    workTimeEnd: QtWidgets.QTimeEdit
    breakTimeStart: QtWidgets.QTimeEdit
    breakTimeEnd: QtWidgets.QTimeEdit
    appointmentTime: QtWidgets.QSpinBox
    appointmentBreakTime: QtWidgets.QSpinBox
    dailyAppointmentLimit: QtWidgets.QSpinBox
    pushButton: QtWidgets.QPushButton

    def __init__(self, parent, doctor):
        super().__init__()
        self.parent = parent
        self.doctor = doctor
        uic.loadUi(
            absolute_asset_path("ui/add_appointment_date.ui"),
            self,
        )
        self.setWindowIcon(icon)
        self.closeEvent = self.closed
        self.pushButton.clicked.connect(self.add_appointment_date)
        self.setFixedSize(400, 420)
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        self.workDateStart.setDate(next_workday(datetime.today()))
        self.workDateEnd.setDate(next_workday(datetime.today()))
        self.show()

    def closed(self, event):
        self.parent.show()
        event.accept()

    def add_appointment_date(self):
        if self.workDateStart.date() > self.workDateEnd.date():
            err("Başlangıç tarihi bitiş tarihinden büyük olamaz.")
            return
        if self.workTimeStart.time() > self.workTimeEnd.time():
            err("Başlangıç saati bitiş saatinde büyük olamaz.")
            return
        if self.breakTimeStart.time() > self.breakTimeEnd.time():
            err("Mola başlangıç saati mola bitiş saatinde büyük olamaz.")
            return
        appointment_dates = []
        for date in daterange(
            self.workDateStart.date().toPyDate(), self.workDateEnd.date().toPyDate()
        ):
            if date.weekday() == 5 or date.weekday() == 6:
                continue
            appointment_count = 0
            for time in timerange(
                self.workTimeStart.dateTime().toPyDateTime(),
                self.workTimeEnd.dateTime().toPyDateTime(),
                self.breakTimeStart.dateTime().toPyDateTime(),
                self.breakTimeEnd.dateTime().toPyDateTime(),
                self.appointmentBreakTime.value(),
                self.appointmentTime.value(),
            ):
                appointment_dates.append(datetime.combine(date, time.time()))
                appointment_count += 1
                if appointment_count == self.dailyAppointmentLimit.value():
                    break

        if appointment_dates:
            self.setEnabled(False)
            self.appointment_dates_ui = AppointmentDatesToAdd(self, appointment_dates)
            if self.appointment_dates_ui.exec_():
                listField = self.doctor.appointment_dates
                for date in appointment_dates:
                    listField.append(AppointmentDate(date=date))
                self.doctor.save()
                info(text="Randevu tarihleri başarıyla eklendi.")
                self.close()
            self.setEnabled(True)
        else:
            err("Randevu tarihleri eklenemedi.")
