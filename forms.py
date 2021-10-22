from flask_wtf import FlaskForm
from wtforms import StringField 
from wtforms.fields.core import IntegerField

class WorkerForm(FlaskForm):
    id = IntegerField(
        'id'
    )
    name = StringField(
        'name'
    )
    surname = StringField(
        'surname'
    )
    birth_date = IntegerField(
        'birth_date'
    )
