import codecs
from typing import Optional
from PyQt5 import QtGui
from PyQt5.QtWidgets import QMessageBox
from importlib import import_module
from utils import absolute_asset_path, icon


def message_box(
    text: Optional[str],
    informative_text=None,
    title="Hastane Randevu",
    box_icon=QMessageBox.Information,
) -> QMessageBox:
    msg = QMessageBox()
    msg.setWindowIcon(icon)
    msg.setIcon(box_icon)
    msg.setText(text)
    msg.setInformativeText(informative_text)
    msg.setWindowTitle(title)
    return msg


def err(text: Optional[str], informative_text=None, title="Hata"):
    message_box(text, informative_text, title, QMessageBox.Critical).exec_()


def info(text: Optional[str], informative_text=None, title="Hastane Randevu"):
    message_box(text, informative_text, title, QMessageBox.Information).exec_()


def yesno(text: Optional[str], informative_text=None, title="Hastane Randevu"):
    message: QMessageBox = message_box(
        text, informative_text, title, QMessageBox.Question
    )
    message.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    return message.exec_() == QMessageBox.Yes


def LazyPage(page_name, *args, **kwargs):
    page = getattr(import_module("ui"), page_name)
    return page(*args, **kwargs)
