import base64
import io

from flask import render_template, flash, redirect, url_for
from matplotlib.figure import Figure

from app import app
from app.forms import LoginForm, SignalGenerationForm
from app.signal_generation import generate_signal


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'alo'}
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

@app.route('/login',  methods=['GET', 'POST'])
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

    if form.validate_on_submit():
        # Recalculate and redraw plot

        signal = generate_signal(form.sample_rate_field.data, form.frequency_field.data, form.duration.data,
                        False)

        embedded_image = create_plot(signal)




    return render_template('generate.html', plot=embedded_image, form=form)



def create_plot(signal):

    # ======= DRAW PLOT ====== #
    fig = Figure()
    ax = fig.subplots()
    ax.plot(signal)
    # Save it to a temporary buffer.
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")

    embedded_image = f"data:image/png;base64,{data}"
    # ======= DRAW PLOT ====== #

    return embedded_image
