from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FieldList, FormField
from wtforms.validators import DataRequired

class GetUsername(FlaskForm):
    username = StringField(
        "Twitter username", validators=[DataRequired()]
    )