from flask import render_template, flash, redirect, url_for, request

from app import app, generated_signals_history, peaks_frequency_estimation
from app.dft_calculation import plot_dft, calculate_fft
from app.forms import LoginForm, SignalGenerationForm, DFTCalculationForm, FrequencyEstimationForm, PeakSelectForm
from app.frequency_estimation import estimate_initial_frequency, signal_crop_estimation
from app.signal_generation import generate_signal, create_plot


selected_index = None


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Alex Farcas'}
    posts = [
        {
            'author': {'username': 'Dumitru farcas'},
            'body': 'Semnalele sunt mai faine decat taragoturile'
        },
        {
            'author': {'username': 'Jean Moscopol'},
            'body': 'O aplicatie buna'
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
    generate_signal(1000, [4.54, 44.33], 1.1, [1, 1], [0, 0, 0], save=True)

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


@app.route('/fft', methods=['GET', 'POST'])
def fft():
    form = DFTCalculationForm()

    # Populate the choices list with the saved signals
    form.select_signal.choices = [(i, signal[1]) for i, signal
                                  in enumerate(generated_signals_history)]

    embedded_image = []

    if form.validate_on_submit():
        signal_selected_index = form.select_signal.data
        selected_signal = generated_signals_history[signal_selected_index]

        # Calculate the DFT
        signal_dft = calculate_fft(selected_signal)

        embedded_image = plot_dft(signal_dft, selected_signal[3])

    return render_template('fft.html', plot=embedded_image, signals=generated_signals_history, form=form)


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
    global selected_index

    if form.estimate_frequency.data and form.validate():

        selected_index = form.select_signal.data
        selected_signal_object = generated_signals_history[selected_index]

        # Estimate the frequency
        embedded_image, peaks = estimate_initial_frequency(selected_signal_object,
                                                           form.start_freq_field.data,
                                                           form.end_freq_field.data)

        peaks_frequency_estimation.clear()
        peaks_frequency_estimation.append(peaks)


    if peaks_frequency_estimation:
        peak_form.select_peak.choices = [(i, "Peak " + str(i)) for i, peak
                                         in enumerate(peaks_frequency_estimation[0])]
        # Reactivate the peak form
        peak_form.submit_choice.render_kw = {}
        peak_form.select_peak.render_kw = {}


    if peak_form.submit_choice.data and peak_form.validate():

        selected_signal_object = generated_signals_history[selected_index]
        chosen_peak = peaks_frequency_estimation[0][peak_form.select_peak.data]
        embedded_image = signal_crop_estimation(selected_signal_object[2][0], selected_signal_object[3], chosen_peak)

    return render_template('frequency_estimation.html', plot=embedded_image,
                           signals=generated_signals_history, form=form, peak_form=peak_form)
