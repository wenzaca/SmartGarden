#!/usr/bin/env python3

import os

if os.path.isdir('../log') is False:
    os.mkdir('../log')

from src.flaskapp import app

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, use_reloader=False, debug=False)
