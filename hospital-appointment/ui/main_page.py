from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt
from ui.ui_utils import LazyPage, err
from ui.make_appointment_page import MakeAppointmentPage
from ui.appointments_page import AppointmentsPage
from ui.doctors_page import DoctorsPage
from utils import absolute_asset_path, icon


class MainPage(QtWidgets.QMainWindow):
    menubar: QtWidgets.QMenuBar
    menuAdmin: QtWidgets.QMenu
    dummy: QtWidgets.QMenu
    menu_Cikis_Yap: QtWidgets.QMenu
    actionRandevu_Al: QtWidgets.QAction
    actionRandevularim_Listele: QtWidgets.QAction
    actionDoktorlar_Listele: QtWidgets.QAction

    def __init__(self, user):
        super().__init__()
        self.user = user
        uic.loadUi(
            absolute_asset_path("ui/main_page.ui"),
            self,
        )
        self.setWindowIcon(icon)
        self.setFixedSize(518, 342)
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)

        self.actionRandevu_Al.triggered.connect(self.open_appointment_page)
        self.actionRandevularim_Listele.triggered.connect(
            self.open_list_appointment_page
        )
        self.actionDoktorlar_Listele.triggered.connect(self.open_doctor_page)
        if user.is_admin:
            # TODO: This is really bad idea, but best solution in limited time.
            # Don't judge me.
            self.dummy.setTitle(
                "                                                                                                            "  # noqa #E501
            )
        else:
            self.actionDoktorlar_Listele.setVisible(False)
            self.menuAdmin.setTitle("")
            # TODO: This is really bad idea, but best solution in limited time.
            # Don't judge me.
            self.dummy.setTitle(
                "                                                                                                                             "  # noqa #E501
            )
        self.menu_Cikis_Yap.mouseReleaseEvent = self.logout
        self.show()

    def open_appointment_page(self):
        print("Randevu Al")
        self.hide()
        self.appointment_page = MakeAppointmentPage(self, self.user)

    def open_list_appointment_page(self):
        print("Randevularım Listele")
        if len(self.user.appointments) == 0:
            err("Randevunuz bulunmamaktadır.")
            return
        self.hide()
        self.appointments = AppointmentsPage(self, self.user)

    def open_doctor_page(self):
        print("Doktorlar Listele")
        self.hide()
        self.doctors = DoctorsPage(self)

    def logout(self, event):
        print("Çıkış Yap")
        self.close()
        self.parent = LazyPage("FirstPage")
