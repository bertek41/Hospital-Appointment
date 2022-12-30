from mongoengine import (
    StringField,
    IntField,
    BooleanField,
    EmbeddedDocumentListField,
    Document,
    DateField,
)
from .appointment import Appointment


class User(Document):
    tc = StringField(max_length=11, required=True)
    name = StringField(max_length=41, required=True)
    surname = StringField(max_length=41, required=True)
    birth_date = DateField(required=True)
    password = StringField(max_length=64, required=True)
    is_admin = BooleanField(default=False)
    appointments = EmbeddedDocumentListField(Appointment)

    meta = {"indexes": [{"fields": ["tc"], "unique": True}]}
