from datetime import timedelta
import os

import pyscrypt
from decouple import config
from PyQt5 import QtGui


def pass_hash(password) -> str:
    return pyscrypt.hash(
        bytes(password, encoding="utf-8"),
        bytes(config("SALT"), encoding="utf-8"),
        1024,
        1,
        1,
        32,
    ).hex()


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)


def timerange(
    start_time, end_time, start_lunch_time, end_lunch_time, break_time, appointment_time
):
    for n in range(
        0, int((end_time - start_time).seconds / 60), appointment_time + break_time
    ):
        time = start_time + timedelta(minutes=n)
        if start_lunch_time <= time < end_lunch_time:
            continue
        yield time


def next_workday(date):
    if date.weekday() == 4:
        return date + timedelta(days=3)
    elif date.weekday() == 5:
        return date + timedelta(days=2)
    else:
        return date + timedelta(days=1)


def absolute_path(relative_path):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)


def absolute_asset_path(relative_path):
    return os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), relative_path
    )


icon = QtGui.QIcon(absolute_asset_path("ui/icons/icon.jpg"))
