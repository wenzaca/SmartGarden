import os

from flask import Flask

this_dir, this_filename = os.path.split(__file__)
template_path = os.path.join(os.path.dirname(this_dir), "flaskapp", "templates")
static_path = os.path.join(os.path.dirname(this_dir), "flaskapp", "static")

app = Flask("SmartGarden Webserver", template_folder=template_path, static_folder=static_path, static_url_path="/static")
app.secret_key = os.urandom(12)

from . import routes
