from app import db
import datetime
from flask_mongoengine.wtf.orm import model_fields, model_form
from flask_wtf import Form


class Todo(db.Document):
    content = db.StringField(required=True, max_length=20)
    time = db.DateTimeField(default=datetime.datetime.now())
    status = db.IntField(default=0)

TodoForm = model_form(Todo)