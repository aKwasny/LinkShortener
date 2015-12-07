# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, session
from uuid import uuid4
import time

app_url = '/kwasiboa/session'
app = Flask(__name__)
app.secret_key = 'J()@#_R MU$*(_U$#*(T'

from werkzeug.debug import DebuggedApplication

app.debug = True
app.wsgi_app = DebuggedApplication(app.wsgi_app, True)


@app.route(app_url + '/')
def index():
    if 'username' not in session:
        return redirect(app_url + '/login')
    username = session['username']
    return render_template('login_success.html', username=username)


@app.route(app_url + '/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login_form.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'akwasny' and password == 'akwasny':
            session['uid'] = uuid4()
            #	uid - unikalny identyfikator
            session['username'] = username
            return render_template('login_success.html', username=username)
        return render_template('login_failure.html', username=username)


# funkcja na razie prototypowa
@app.route(app_url + '/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register_form.html')
    if request.method == 'POST':
        username = request.form.get('login')
        password = request.form.get('password')
        return render_template('register_success.html', username=username)
        print "Sukces! Za 8 sekund zostaniesz przeniesiony do strony logowania"
        time.sleep(8)
        return redirect(app_rul + '/login_form.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
