from mongoengine import StringField, EmbeddedDocumentListField, Document
from .appointments_date import AppointmentDate


class Doctor(Document):
    name = StringField(max_length=81, required=True)
    city = StringField(max_length=41, required=True)
    county = StringField(max_length=41, required=True)
    clinic = StringField(max_length=41, required=True)
    hospital = StringField(max_length=100, required=True)
    appointment_dates = EmbeddedDocumentListField(AppointmentDate)

    meta = {"indexes": ["clinic"]}

    @property
    def available_appointments(self):
        return [
            appointment
            for appointment in self.appointment_dates
            if appointment.is_available
        ]
