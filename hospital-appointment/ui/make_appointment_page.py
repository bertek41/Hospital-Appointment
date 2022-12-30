from datetime import datetime, timedelta

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt
from ui.ui_utils import err
from ui.select_doctor_page import SelectDoctor
from models import Doctor
from utils import absolute_asset_path, icon


class MakeAppointmentPage(QtWidgets.QDialog):
    cityBox: QtWidgets.QComboBox
    countyBox: QtWidgets.QComboBox
    clinicBox: QtWidgets.QComboBox
    hospitalBox: QtWidgets.QComboBox
    startDate: QtWidgets.QDateEdit
    endDate: QtWidgets.QDateEdit
    searchButton: QtWidgets.QPushButton

    def __init__(self, parent, user):
        super().__init__()
        self.parent = parent
        self.user = user
        uic.loadUi(
            absolute_asset_path("ui/make_appointment_page.ui"),
            self,
        )
        self.setWindowIcon(icon)
        self.setFixedSize(383, 313)
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        self.startDate.setDate(datetime.today())
        self.endDate.setDate(datetime.today() + timedelta(days=14))
        self.doctors = Doctor.objects()
        cities = []

        for doctor in self.doctors:
            if doctor.city not in cities:
                cities.append(doctor.city)

        self.cityBox.addItems(cities)
        self.cityBox.setCurrentIndex(-1)
        self.cityBox.currentTextChanged.connect(self.city_changed)
        self.searchButton.clicked.connect(self.search)

        self.closeEvent = self.closed
        self.show()

    def closed(self, event):
        self.parent.show()
        event.accept()

    def search(self):
        print("search")
        if self.cityBox.currentIndex() == -1:
            err("Lütfen bir şehir seçiniz.")
            return
        if self.countyBox.currentIndex() == -1:
            err("Lütfen bir ilçe seçiniz.")
            return
        if self.clinicBox.currentIndex() == -1:
            err("Lütfen bir klinik seçiniz.")
            return
        if self.hospitalBox.currentIndex() == -1:
            err("Lütfen bir hastane seçiniz.")
            return
        if self.startDate.date() > self.endDate.date():
            err("Başlangıç tarihi bitiş tarihinden büyük olamaz.")
            return
        doctors = Doctor.objects(
            city=self.cityBox.currentText(),
            county=self.countyBox.currentText(),
            clinic=self.clinicBox.currentText(),
            hospital=self.hospitalBox.currentText(),
        ).all()
        if len(doctors) == 0:
            err("Aradığınız kriterlere uygun doktor bulunamadı.")
            return
        self.hide()
        self.select_doctor_date = SelectDoctor(
            self,
            self.user,
            doctors,
            self.startDate.date().toPyDate(),
            self.endDate.date().toPyDate(),
        )

    def clear_box(self, row):
        self.countyBox.blockSignals(True)
        self.clinicBox.blockSignals(True)
        self.hospitalBox.blockSignals(True)
        if row == 0:
            self.countyBox.clear()
            self.countyBox.setCurrentIndex(-1)
            self.clinicBox.clear()
            self.clinicBox.setCurrentIndex(-1)
            self.hospitalBox.clear()
            self.hospitalBox.setCurrentIndex(-1)
        elif row == 1:
            self.clinicBox.clear()
            self.clinicBox.setCurrentIndex(-1)
            self.hospitalBox.clear()
            self.hospitalBox.setCurrentIndex(-1)
        elif row == 2:
            self.hospitalBox.clear()
            self.hospitalBox.setCurrentIndex(-1)
        self.countyBox.blockSignals(False)
        self.clinicBox.blockSignals(False)
        self.hospitalBox.blockSignals(False)

    def city_changed(self, city):
        print("city changed", city)

        counties = []
        for doctor in self.doctors:
            if doctor.city == city and doctor.county not in counties:
                counties.append(doctor.county)

        try:
            self.countyBox.currentTextChanged.disconnect()
        except TypeError:
            pass
        self.clear_box(0)
        self.countyBox.addItems(counties)
        self.countyBox.setCurrentIndex(-1)
        self.countyBox.currentTextChanged.connect(
            lambda county: self.county_changed(city, county)
        )

    def county_changed(self, city, county):
        print("county changed", city, county)

        clinics = []
        for doctor in self.doctors:
            if (
                doctor.city == city
                and doctor.county == county
                and doctor.clinic not in clinics
            ):
                clinics.append(doctor.clinic)

        try:
            self.clinicBox.currentTextChanged.disconnect()
        except TypeError:
            pass
        self.clear_box(1)
        self.clinicBox.addItems(clinics)
        self.clinicBox.setCurrentIndex(-1)
        self.clinicBox.currentTextChanged.connect(
            lambda clinic: self.clinic_changed(city, county, clinic)
        )

    def clinic_changed(self, city, county, clinic):
        print("clinic changed", city, county, clinic)

        hospitals = []
        longest_word = ""
        for doctor in self.doctors:
            if (
                doctor.city == city
                and doctor.county == county
                and doctor.clinic == clinic
                and doctor.hospital not in hospitals
            ):
                hospitals.append(doctor.hospital)
                if len(doctor.hospital) > len(longest_word):
                    longest_word = doctor.hospital

        try:
            self.hospitalBox.currentTextChanged.disconnect()
        except TypeError:
            pass
        self.clear_box(2)
        self.hospitalBox.addItems(hospitals)
        self.hospitalBox.view().setMinimumWidth(
            self.hospitalBox.view().fontMetrics().boundingRect(longest_word).width()
        )
        self.hospitalBox.setCurrentIndex(-1)
