from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, FloatField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):

    username = StringField(label='Username', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    remember_me = BooleanField(label='Remember Me')
    submit = SubmitField(label='Sign In')


class SignalGenerationForm(FlaskForm):

    sample_rate_field = IntegerField(label='Sample Rate', default=100)
    frequency_field1 = FloatField(label='Frequency 1', default=0)
    frequency_field2 = FloatField(label='Frequency 2', default=0)
    frequency_field3 = FloatField(label='Frequency 3', default=0)
    duration = FloatField(label='Duration (s)', default=1)
    useCos = BooleanField(label='Use cos function (sin by default)')
    generate = SubmitField(label='Generate Signal')



