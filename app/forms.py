from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, FloatField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):

    username = StringField(label='Username', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    remember_me = BooleanField(label='Remember Me')
    submit = SubmitField(label='Sign In')


class SignalGenerationForm(FlaskForm):

    sample_rate_field = IntegerField(label='Sample Rate')
    frequency_field = FloatField(label='Frequency')
    duration = FloatField(label='Duration (s)')
    useCos = BooleanField(label='Use cos function')
    generate = SubmitField(label='Generate Signal')



