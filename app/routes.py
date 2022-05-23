import requests
from flask import render_template, flash, redirect, url_for, request

from app import app, generated_signals_history, peaks_frequency_estimation
from app.dft_calculation import plot_dft, calculate_dft
from app.forms import LoginForm, SignalGenerationForm, DFTCalculationForm, FrequencyEstimationForm, PeakSelectForm
from app.frequency_estimation import estimate_frequency
from app.signal_generation import generate_signal, create_plot


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Handicapatul'}
    posts = [
        {
            'author': {'username': 'ElChapo'},
            'body': 'Cat e ceasu!'
        },
        {
            'author': {'username': 'JeanValjean'},
            'body': 'da domnule'
        }
    ]
    return render_template('index.html', title='Homepage', user=user, posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/generate', methods=['GET', 'POST'])
def signal_generator():
    form = SignalGenerationForm()

    embedded_image = []

    # Mock
    generate_signal(100, [4.54, 53.33], 1, [1, 1], [0, 0, 0], save=True)

    if form.validate_on_submit():
        # Recalculate and redraw plot

        frequency_array = [form.frequency_field1.data,
                           form.frequency_field2.data,
                           form.frequency_field3.data]

        amplitude_array = [form.amplitude_field1.data,
                           form.amplitude_field2.data,
                           form.amplitude_field3.data]

        phase_array = [form.phase_field1.data,
                       form.phase_field2.data,
                       form.phase_field3.data]

        # Remove negative values and zeroes
        frequency_array = [i for i in frequency_array if i >= 0]
        amplitude_array = [i for i in amplitude_array if i >= 0]

        (signal, time_range) = generate_signal(form.sample_rate_field.data, frequency_array,
                                               form.duration.data, amplitude_array, phase_array,
                                               form.useCos.data, normalize=form.normalize.data, save=form.save.data)

        embedded_image = create_plot(signal, time_range)

    return render_template('generate.html', plot=embedded_image, form=form)


@app.route('/dft', methods=['GET', 'POST'])
def dft():
    form = DFTCalculationForm()

    # Populate the choices list with the saved signals
    form.select_signal.choices = [(i, signal[1]) for i, signal
                                  in enumerate(generated_signals_history)]

    embedded_image = []

    if form.validate_on_submit():
        selected_index = form.select_signal.data
        selected_signal = generated_signals_history[selected_index]

        # Calculate the DFT
        signal_dft = calculate_dft(selected_signal)

        embedded_image = plot_dft(signal_dft, selected_signal[3])

    return render_template('dft.html', plot=embedded_image, signals=generated_signals_history, form=form)


@app.route('/estimate', methods=['GET', 'POST'])
def frequency_estimation():
    form = FrequencyEstimationForm()
    peak_form = PeakSelectForm()

    # Disable the peak form
    peak_form.submit_choice.render_kw = {'disabled': 'disabled'}
    peak_form.select_peak.render_kw = {'disabled': 'disabled'}

    # Populate the selects
    form.select_signal.choices = [(i, signal[1]) for i, signal
                                  in enumerate(generated_signals_history)]




    embedded_image = []

    if form.validate_on_submit():
        selected_index = form.select_signal.data
        selected_signal = generated_signals_history[selected_index]

        # Estimate the frequency
        embedded_image, peaks = estimate_frequency(selected_signal)

        peaks_frequency_estimation.append(peaks)


    if peaks_frequency_estimation:
        peak_form.select_peak.choices = [(peak, "Peak " + str(i)) for i, peak
                                         in enumerate(peaks_frequency_estimation[0])]
        # Reactivate the peak form
        peak_form.submit_choice.render_kw = {}
        peak_form.select_peak.render_kw = {}


    if peak_form.select_peak.data and peak_form.validate_on_submit():
        print("da")


    return render_template('frequency_estimation.html', plot=embedded_image,
                           signals=generated_signals_history, form=form, peak_form=peak_form)
