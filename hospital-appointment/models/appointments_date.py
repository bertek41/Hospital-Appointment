import mongoengine as mango


class AppointmentDate(mango.EmbeddedDocument):
    date = mango.DateTimeField(required=True)
    is_available = mango.BooleanField(default=True)
