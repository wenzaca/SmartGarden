import sys

import boto3
from flask import render_template, url_for, redirect, request, jsonify, session

from src import jsonconverter as jsonc, repository_dynamo, log_util
from src.flaskapp import app
from src.flaskapp.forms import LoginForm

cognito = client = boto3.client('cognito-idp')


# login
@app.route("/login", methods=['GET', 'POST'])
def login():
    if session.get('logged_in'):
        return redirect(url_for('dashboard'))
    else:
        form = LoginForm()
        if form.validate_on_submit():
            try:
                cognito.admin_initiate_auth(AuthFlow='ADMIN_NO_SRP_AUTH',
                                            AuthParameters={
                                                'USERNAME': form.username.data,
                                                'PASSWORD': form.password.data
                                            },
                                            ClientId='2v3e93opl3akulijav5eusliov',
                                            UserPoolId='eu-west-1_g70ijojs5')
                session['logged_in'] = True
                log_util.log_debug(__name__, "User Logged in correctly, username: {}".format(form.username.data))
                return redirect(url_for('dashboard'))
            except (cognito.exceptions.NotAuthorizedException, cognito.exceptions.UserNotFoundException) as e:
                log_util.log_error(__name__,
                                   "User not authenticate, username: {}. Error: {}".format(form.username.data, e))
                return render_template('login.html', title='Login', error="Incorrect username or password.", form=form)
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
    if request.method == 'GET':
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
    if request.method == 'GET':
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
