import sys

import jsonconverter as jsonc
import repository
from flask import render_template, url_for, redirect, request, jsonify, session, flash
from flaskapp import app
from flaskapp.forms import LoginForm


# login
@app.route("/login", methods=['GET', 'POST'])
def login():
    if session.get('logged_in'):
        return redirect(url_for('dashboard'))
    else:
        form = LoginForm()
        if form.validate_on_submit():
            data = repository.login()
            for d in data:
                if form.username.data == d['username'] and form.password.data == d['password']:
                    session['logged_in'] = True
                    return redirect(url_for('dashboard'))
                else:
                    flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


# logout
@app.route("/logout")
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))


# pages
@app.route("/")
@app.route("/dashboard")
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        return render_template('dashboard.html', title='Dashboard', active='dashboard')


@app.route("/graph")
def graph():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        return render_template('graph.html', title='Graph', active='graph')


@app.route("/setting")
def setting():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        return render_template('setting.html', title='Settings', active='setting')


# api routes
@app.route("/api/getMaxData", methods=['POST', 'GET'])
def api_getMaxData():
    if request.method == 'POST':
        try:
            data = jsonc.json.loads(request.data)
            if data['moisture'] is not '':
                repository.post_max_data(data)

            return str(data)
        except:
            print(sys.exc_info()[0])
            print(sys.exc_info()[1])
            return None
    elif request.method == 'GET':
        try:
            data = jsonc.data_to_json(repository.get_max_data())
            loaded_data = jsonc.json.loads(data)
            return jsonify(loaded_data)
        except:
            print(sys.exc_info()[0])
            print(sys.exc_info()[1])
            return None


# api routes
@app.route("/api/getData", methods=['POST', 'GET'])
def api_getData():
    if request.method == 'POST':
        try:
            data = jsonc.data_to_json(repository.get_data())
            loaded_data = jsonc.json.loads(data)
            # print(loaded_data)
            return jsonify(loaded_data)
        except:
            print(sys.exc_info()[0])
            print(sys.exc_info()[1])
            return None


@app.route("/api/getChartData", methods=['POST', 'GET'])
def api_getChartData():
    if request.method == 'POST':
        try:
            data = jsonc.data_to_json(repository.get_chart_data())
            loaded_data = jsonc.json.loads(data)
            # print(loaded_data)
            return jsonify(loaded_data)
        except:
            print(sys.exc_info()[0])
            print(sys.exc_info()[1])
            return None


@app.route("/api/status", methods=['GET', 'POST'])
def status():
    try:
        data = jsonc.data_to_json(repository.get_status())
        loaded_data = jsonc.json.loads(data)
        # print(loaded_data)
        return jsonify(loaded_data)

        status = loaded_data[0].status

        return status
    except:
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])
        return None


@app.route("/changeStatus/<status>")
def changeStatus(status):
    try:
        repository.post_status(status)

        return status
    except:
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])
        return None
