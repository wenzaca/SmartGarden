import os

from flask import Flask

app = Flask(__name__)
app.secret_key = os.urandom(12)

from . import routes
