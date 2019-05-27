import sys

import jsonconverter as jsonc
import repository_dynamo
from flask import render_template, url_for, redirect, request, jsonify, session, flash
from flaskapp import app
from flaskapp.forms import LoginForm
import log_util


# login
@app.route("/login", methods=['GET', 'POST'])
def login():
    if session.get('logged_in'):
        return redirect(url_for('dashboard'))
    else:
        form = LoginForm()
        if form.validate_on_submit():
            data = repository_dynamo.login()
            for d in data:
                if form.username.data == d['username'] and form.password.data == d['password']:
                    session['logged_in'] = True
                    log_util.log_debug(__name__, "User Logged in correctly, username: {}".format(d['username']))
                    return redirect(url_for('dashboard'))
                else:
                    log_util.log_debug(__name__, "User not authenticate, username: {}".format(d['username']))
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
                log_util.log_debug(__name__, "Received max data, sending to DynamoDB: {}".format(str(data)))
                repository_dynamo.post_max_data(data)

            return str(data)
        except:
            log_util.log_error(__name__, sys.exc_info()[0])
            log_util.log_error(__name__, sys.exc_info()[1])
            return None
    elif request.method == 'GET':
        try:
            data = jsonc.data_to_json(repository_dynamo.get_max_data())
            loaded_data = jsonc.json.loads(data)
            log_util.log_debug(__name__, "Getting max data from DynamoDB: {}".format(str(loaded_data)))
            return jsonify(loaded_data)
        except:
            log_util.log_error(__name__, sys.exc_info()[0])
            log_util.log_error(__name__, sys.exc_info()[1])
            return None


# api routes
@app.route("/api/getData", methods=['POST', 'GET'])
def api_getData():
    if request.method == 'POST':
        try:
            data = jsonc.data_to_json(repository_dynamo.get_data())
            loaded_data = jsonc.json.loads(data)
            log_util.log_debug(__name__, "Getting readings data from DynamoDB: {}".format(str(loaded_data)))
            return jsonify(loaded_data)
        except:
            log_util.log_error(__name__, sys.exc_info()[0])
            log_util.log_error(__name__, sys.exc_info()[1])
            return None


@app.route("/api/getChartData", methods=['POST', 'GET'])
def api_getChartData():
    if request.method == 'POST':
        try:
            data = jsonc.data_to_json(repository_dynamo.get_chart_data())
            loaded_data = jsonc.json.loads(data)
            log_util.log_debug(__name__, "Getting chart data from DynamoDB: {}".format(str(loaded_data)))
            return jsonify(loaded_data)
        except:
            log_util.log_error(__name__, sys.exc_info()[0])
            log_util.log_error(__name__, sys.exc_info()[1])
            return None


@app.route("/api/status", methods=['GET', 'POST'])
def status():
    try:
        data = jsonc.data_to_json(repository_dynamo.get_status())
        loaded_data = jsonc.json.loads(data)
        log_util.log_debug(__name__, "Getting status from DynamoDB: {}".format(str(loaded_data)))
        return jsonify(loaded_data)
    except:
        log_util.log_error(__name__, sys.exc_info()[0])
        log_util.log_error(__name__, sys.exc_info()[1])
        return None


@app.route("/changeStatus/<status>")
def changeStatus(status):
    try:
        log_util.log_debug(__name__, "Received status change request, sending to DynamoDB: {}".format(str(status)))
        repository_dynamo.post_status(status)
        return status
    except:
        log_util.log_error(__name__, sys.exc_info()[0])
        log_util.log_error(__name__, sys.exc_info()[1])
        return None
