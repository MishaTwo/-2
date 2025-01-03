from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class RegistrationForm(FlaskForm):
    username = StringField("Ім'я користувача: ", validators=[DataRequired()])
    email = StringField('Емейл: ', validators=[DataRequired()])
    password = StringField('Пароль: ', validators=[DataRequired()])
    submit = SubmitField("Зареєструватися")