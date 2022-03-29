import base64
import io

from flask import render_template, flash, redirect, url_for
from matplotlib.figure import Figure

from app import app
from app.forms import LoginForm


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Bai'}
    posts = [
        {
            'author': {'username': 'UnBoacter'},
            'body': 'Cat e ceasu!'
        },
        {
            'author': {'username': 'UnFraier'},
            'body': '!'
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


@app.route('/generate')
def signal_generator():

    fig = Figure()
    ax = fig.subplots()
    ax.plot([1, 2])
    # Save it to a temporary buffer.
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")

    embedded_image = f"data:image/png;base64,{data}"

    return render_template('generate.html', plot=embedded_image)
