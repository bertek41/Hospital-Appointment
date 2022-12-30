from PyQt5 import QtWidgets, QtGui, uic
from PyQt5.QtCore import Qt
from utils import absolute_asset_path, icon


class AppointmentDatesToAdd(QtWidgets.QDialog):
    listView: QtWidgets.QListView
    confirmButton: QtWidgets.QPushButton
    cancelButton: QtWidgets.QPushButton

    def __init__(self, parent, dates):
        super().__init__()
        self.parent = parent
        self.dates = dates
        uic.loadUi(
            absolute_asset_path("ui/appointment_dates_to_add.ui"),
            self,
        )
        self.setWindowIcon(icon)
        model = QtGui.QStandardItemModel()
        self.listView.setModel(model)
        for date in dates:
            item = QtGui.QStandardItem(date.strftime("%d.%m.%Y %H:%M"))
            item.setTextAlignment(Qt.AlignCenter)
            model.appendRow(item)

        self.closeEvent = self.closed
        self.confirmButton.clicked.connect(self.confirm)
        self.cancelButton.clicked.connect(self.cancel)
        self.setFixedSize(275, 362)
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        self.show()

    def closed(self, event):
        self.parent.show()
        event.accept()

    def confirm(self):
        self.accept()

    def cancel(self):
        self.reject()
