#!/usr/bin/env python3

from flaskapp import app

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=80, use_reloader=False, debug=False)
