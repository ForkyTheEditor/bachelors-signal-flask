from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, FloatField, SelectField
from wtforms.validators import DataRequired

from app import generated_signals_history


class LoginForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    remember_me = BooleanField(label='Remember Me')
    submit = SubmitField(label='Sign In')


class SignalGenerationForm(FlaskForm):
    sample_rate_field = IntegerField(label='Sample Rate', default=1000)
    frequency_field1 = FloatField(label='Frequency 1', default=0)
    frequency_field2 = FloatField(label='Frequency 2', default=0)
    frequency_field3 = FloatField(label='Frequency 3', default=0)
    amplitude_field1 = FloatField(label='Amplitude 1', default=1)
    amplitude_field2 = FloatField(label='Amplitude 2', default=0)
    amplitude_field3 = FloatField(label='Amplitude 3', default=0)
    phase_field1 = FloatField(label='Phase 1', default=0)
    phase_field2 = FloatField(label='Phase 2', default=0)
    phase_field3 = FloatField(label='Phase 3', default=0)
    duration = FloatField(label='Duration (s)', default=1)
    useCos = BooleanField(label='Use cos function (sin by default)')
    normalize = BooleanField(label='Normalize')
    save = BooleanField(label='Save signal to cache')
    generate = SubmitField(label='Generate Signal')


class DFTCalculationForm(FlaskForm):
    select_signal = SelectField(label="Select Signal", coerce=int)
    calculate_dft = SubmitField(label='Calculate DFT')


class FrequencyEstimationForm(FlaskForm):

    select_signal = SelectField(label="Select Signal", coerce=int)
    start_freq_field = IntegerField(label='Start frequency', default=0)
    end_freq_field = IntegerField(label='End frequency', default=50)
    estimate_frequency = SubmitField(label='Estimate Frequency (DFT)')


class PeakSelectForm(FlaskForm):

    select_peak = SelectField(label="Select Peak", coerce=int)
    submit_choice = SubmitField(label="Calculate around peak")
