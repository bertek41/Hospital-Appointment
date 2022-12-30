import sys

from PyQt5 import QtWidgets, QtGui
from decouple import config
from mongoengine import connect


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    connect(host=config("DATABASE_URL"))
    sys.excepthook = except_hook
    app = QtWidgets.QApplication(sys.argv)
    from utils import icon, absolute_asset_path
    from ui import LazyPage

    application = LazyPage("FirstPage")
    app.exec_()
