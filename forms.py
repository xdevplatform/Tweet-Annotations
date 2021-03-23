from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FieldList, FormField
from wtforms.validators import DataRequired


class GetUsername(FlaskForm):
    username = StringField(
        "Insert a Twitter username below:", validators=[DataRequired()]
    )


class GetKeyword(FlaskForm):
    keyword = StringField(
        "Insert a topic or phrase of interest below (e.g. skiing):",
        validators=[DataRequired()],
    )


class GetTopic(FlaskForm):
    topic = StringField(
        "Annotation (e.g. Web development)", validators=[DataRequired()]
    )


class DropdownForm(FlaskForm):
    select = SelectField("", choices=[], validators=[DataRequired()])
