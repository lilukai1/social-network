from flask import (Flask, g, render_template, flash, redirect, url_for)
from flask_login import LoginManager

import forms
import models

DEBUG = True
PORT = 8000
HOST = '127.0.0.1'

app = Flask(__name__)
app.secret_key = 'klsdhgaowihgwaeongvsbldkhgaowiah'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None

@app.before_request
def before_request():
    g.db = models.DATABASE
    g.db.connect()

@app.after_request
def after_request(response):
    g.db.close()
    return response

@app.route('/register/', methods=('GET', 'POST'))
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        flash("Yay, you registered!", "success")
        models.User.create_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )
        return redirect(url_for('index'))
    return render_template('register.html', form=form)

@app.route('/', methods=('GET', 'POST'))
def index():
    return render_template('index.html')





if __name__ == '__main__':
    models.initialize()
    try:
        models.User.create_user(
            username='anniewiley',
            email='annienwiley@gmail.com',
            password='password',
            admin=True

        )
    except ValueError:
        pass
    app.run(debug=DEBUG, port=PORT, host=HOST)