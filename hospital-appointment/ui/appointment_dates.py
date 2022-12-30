from datetime import datetime
from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtCore import Qt
from ui.ui_utils import err, info
from models import AppointmentDate
from utils import absolute_asset_path, icon


class AppointmentDates(QtWidgets.QDialog):
    tableWidget: QtWidgets.QTableWidget
    dateTimeEdit: QtWidgets.QDateTimeEdit
    addDateTimeButton: QtWidgets.QPushButton
    deleteSelectedButton: QtWidgets.QPushButton
    selectAllButton: QtWidgets.QPushButton
    deselectAllButton: QtWidgets.QPushButton
    okButton: QtWidgets.QPushButton

    def __init__(self, parent, doctor):
        super().__init__()
        self.parent = parent
        self.doctor = doctor
        self.appointment_dates = [date.date for date in self.doctor.appointment_dates]
        uic.loadUi(
            absolute_asset_path("ui/appointment_doctor_dates_edit.ui"),
            self,
        )
        self.setWindowIcon(icon)
        self.setFixedSize(400, 320)
        self.update_table()
        self.closeEvent = self.closed
        self.addDateTimeButton.clicked.connect(self.add_date_time)
        self.selectAllButton.clicked.connect(self.select)
        self.deselectAllButton.clicked.connect(self.deselect)
        self.deleteSelectedButton.clicked.connect(self.delete)
        self.okButton.clicked.connect(self.ok)
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        self.show()

    def update_table(self):
        self.tableWidget.clear()
        self.tableWidget.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeToContents
        )
        self.tableWidget.verticalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeToContents
        )
        self.tableWidget.horizontalHeader().setSectionResizeMode(
            0, QtWidgets.QHeaderView.Stretch
        )
        self.tableWidget.setRowCount(len(self.appointment_dates))
        for index, date in enumerate(self.appointment_dates):
            item = QtWidgets.QTableWidgetItem(date.strftime("%d.%m.%Y %H:%M"))
            item.setTextAlignment(Qt.AlignCenter)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            self.tableWidget.setItem(index, 0, item)

    def closed(self, event):
        self.parent.show()
        event.accept()

    def add_date_time(self):
        date_time = self.dateTimeEdit.dateTime().toPyDateTime()
        if date_time in self.appointment_dates:
            err("Bu tarih ve saate ait randevu zaten var.")
            return
        self.appointment_dates.append(date_time)
        self.appointment_dates.sort()
        self.update_table()

    def select(self):
        for i in range(self.tableWidget.rowCount()):
            item = self.tableWidget.item(i, 0)
            item.setCheckState(QtCore.Qt.Checked)

    def deselect(self):
        for i in range(self.tableWidget.rowCount()):
            item = self.tableWidget.item(i, 0)
            item.setCheckState(QtCore.Qt.Unchecked)

    def delete(self):
        choices = [
            i
            for i in range(self.tableWidget.rowCount())
            if self.tableWidget.item(i, 0).checkState() == QtCore.Qt.Checked
        ]
        for index in sorted(choices, reverse=True):
            self.appointment_dates.pop(index)
        self.update_table()

    def ok(self):
        final_choices = []
        for i in range(self.tableWidget.rowCount()):
            item = self.tableWidget.item(i, 0)
            try:
                dt = datetime.strptime(item.text(), "%d.%m.%Y %H:%M")
            except ValueError:
                err(
                    "Hatalı tarih formatı, index={}."
                    "Olması gereken format=%d.%m.%Y %H:%M".format(i)
                )
                return
            else:
                final_choices.append(dt)
        final_choices = [*set(final_choices)]
        if not final_choices:
            self.doctor.appointment_dates.delete()
        else:
            list_field = self.doctor.appointment_dates
            list_field.clear()
            for date in sorted(final_choices):
                self.doctor.appointment_dates.append(AppointmentDate(date=date))
        self.doctor.save()
        info(text="Randevu tarihleri başarıyla güncellendi.")
        self.close()
