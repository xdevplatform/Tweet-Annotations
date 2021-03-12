from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FieldList, FormField
from wtforms.validators import DataRequired

class GetUsername(FlaskForm):
    username = StringField(
        "Twitter username", validators=[DataRequired()]
    )

class GetTopic(FlaskForm):
    topic = StringField(
        "Annotation (e.g. Web development)", validators=[DataRequired()]
    )

class DropdownForm(FlaskForm):
    select = SelectField("", choices=[], validators=[DataRequired()])
