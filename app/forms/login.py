from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    email = StringField('Емейл: ', validators=[DataRequired()])
    submit = SubmitField("Увійти")