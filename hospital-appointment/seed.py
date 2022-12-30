from models import Doctor, AppointmentDate
from datetime import datetime
from mongoengine import connect
from decouple import config


def add_doctor(name, city, county, clinic, hospital):
    doctor = Doctor(
        name=name,
        city=city,
        county=county,
        clinic=clinic,
        hospital=hospital,
    )
    listField = doctor.appointment_dates
    listField.append(AppointmentDate(date=datetime(2022, 12, 1, 10, 0)))
    listField.append(AppointmentDate(date=datetime(2022, 12, 1, 10, 30)))
    listField.append(AppointmentDate(date=datetime(2022, 12, 1, 11, 0)))
    doctor.save()


if __name__ == "__main__":
    connect(host=config("DATABASE_URL"))
    Doctor.objects.delete()
    add_doctor(
        "Ahmet Hamdi Kırkpınar",
        "İstanbul",
        "Zeytinburnu",
        "Fizyoterapi",
        "Zeytinburnu Devlet Hastanesi",
    )
    add_doctor(
        "Cemal Sürahi",
        "Ankara",
        "Yenimahalle",
        "KBB",
        "Yenimahalle Devlet Hastanesi",
    )
    add_doctor("Kemal Namık", "İzmir", "Buca", "Cildiye", "Buca Devlet Hastanesi")
    add_doctor(
        "Tevret Fikfik", "Kocaeli", "Gölcük", "Dahiliye", "Gölcük Devlet Hastanesi"
    )

    """_user_id = randint(11111111111, 99999999999)
    _user = User(
        tc=f"{_user_id}",
        name=f"Ahmet - {_user_id}",
        surname="Hamdi",
        year_born=1990,
        password="123456",
        is_admin=False,
        appointments=[
            Appointment(doctor=_doctor, date=datetime(2022, 10, 18, 10, 0, 0))
        ],
    )

    _user.save()

    print(
        User.objects(appointments__date__gte=datetime(2022, 10, 19, 10, 0, 0))
        .first()
        .name
    )
    print(
        User.objects(**{"appointments__date__gte": datetime(2022, 10, 19, 10, 0, 0)})
        .first()
        .name
    )

    payload = {}

    if "doctor" in parameter:
        payload["appointments__doctor"] = parameter["doctor"]

    if "date" in parameter:
        payload["appointments__date__gte"] = parameter["date"]

    if "date" in parameter:
        payload["appointments__date__lte"] = parameter["date"]

    User.objects(**payload)
    User.objects()
    User.objects(appointments__doctor=parameter["doctor"])
    User.objects(
        appointments__doctor=parameter["doctor"],
        appointments_date__gte=parameter["date"],
    )
    User.objects(
        appointments__doctor=parameter["doctor"],
        appointments_date__lte=parameter["date"],
    )"""
