# -*- coding: utf-8 -*-
import json
import random
import string, time, sqlite3
from math import floor
from flask import Flask, render_template, request, redirect, session
from uuid import uuid4
from urlparse import urlparse
from sqlite3 import OperationalError

app_url = '/kwasiboa/session'
app = Flask(__name__)
app.secret_key = 'J()@#_R MU$*(_U$#*(T'
linkbasename = 'links.txt'
all_links = {}
all_users = {}

from werkzeug.debug import DebuggedApplication

app.debug = False
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
            loggedin = True
            message = u'Zalogowano pomyślnie'
            return render_template('login_success.html', username=username, loggedin=loggedin, message=message)
        else:
            message = u'Błąd logowania.'
            return render_template('login_form.html', username=username, message=message)


def logout():
    session.pop('username', None)
    return redirect("http://edi.iem.pw.edu.pl" + app_url)


@app.route(app_url + '/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register_form.html')
    if request.method == 'POST':
        username = request.form.get('login')
        password = request.form.get('password')
        if username not in all_users:
            all_users[username] = password
            message = u'Zarejestrowano pomyślnie'
        else:
            message = u'Podana nazwa użytkownika jest już zajęta, wybierz proszę inną'
        return render_template('register_success.html', username=username, password=password)




@app.route(app_url + '/shortener', methods=['GET', 'POST'])
def shortener():
    """if 'username' not in session:
        return redirect(app_url + '/login')
    username = session['username']
    return render_template('login_success.html', username=username)"""
    if request.method == 'GET':
        return render_template('shortener.html')
    if request.method == 'POST':
        linktoshorten = request.form.get('linktoshorten')
        shortened_link = 'http://edi.iem.pw.edu.pl' + app_url + '/' + ''.join(
                random.SystemRandom().choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for x in
                range(7))
        savelinktobase(shortened_link, 'links.txt')
        return render_template('link_shortened.html')


@app.route(app_url + '/decrypter', methods=['GET', 'POST'])
def decrypter():
    if request.method == 'GET':
        return render_template('decrypter.html')
    if request.method == 'POST':
        linktodecrypt = request.form.get('linktodecrypt')


def savelinktobase(link, filename):
    with open(filename, 'w') as saving:
        saving.write('%s' % json.dumps(all_links))
        saving.close()


def loadlinkfrombase(link, filename):
    with open(filename, 'r') as loading:
        all_links.update(json.loads(filename.read()))
        loading.close()



if __name__ == '__main__':
    app.run(host='0.0.0.0')
