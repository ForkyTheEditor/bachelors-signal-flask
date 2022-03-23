from flask import render_template
from app import app


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
