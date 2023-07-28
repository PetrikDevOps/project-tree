import importlib
import os

from flask import Flask, render_template, jsonify, request, session
from flask_cors import CORS
from flask_session import Session
from werkzeug.middleware.proxy_fix import ProxyFix

import config
import helpers

helpers_dir = os.path.join(os.path.dirname(__file__), 'helpers')
helper_files = os.listdir(helpers_dir)

for file in helper_files:
    if file.endswith('.py') and file != '__init__.py':
        module_name = os.path.splitext(file)[0]
        module = importlib.import_module(f'helpers.{module_name}')
        setattr(helpers, module_name, module)

app = Flask(__name__)
CORS(app)
app.secret_key = config.SECRET_KEY
app.config.from_pyfile('config.py')
Session(app)

# Fixes some stuff when running on localhost
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)


@app.route('/login', methods=['GET'])
def login():
    session['logged_in'] = True
    return jsonify({'message': 'Login successful!'})

@app.route('/logout', methods=['GET'])
def logout():
    # Clear the 'logged_in' flag from the session
    session.pop('logged_in', None)
    return jsonify({'message': 'Logout successful!'})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5052, debug=True)
