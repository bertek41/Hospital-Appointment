import mongoengine as mango
from bson import ObjectId


class Appointment(mango.EmbeddedDocument):
    id = mango.fields.ObjectIdField(
        unique=True, default=ObjectId, required=True, primary_key=True
    )
    doctor = mango.ReferenceField("Doctor")
    date = mango.DateTimeField(required=True)
