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

@app.route('/projects', methods=['GET'])
def get_projects():
    parsed = []
    for project in helpers.project.get_all_projects():
        project_data = {
            'project_id': project.project_id,
            'name': project.name,
            'state': helpers.phase.get_current_phase(project.project_id),
            'max_team_num': project.max_team_num,
            'current_team_num': len(project.teams),
            'first': 'majd lesz valami',
            'second': 'majd lesz valami',
            'third': 'majd lesz valami',
        }
        parsed.append(project_data)
    return jsonify({'projects': parsed})

#p = helpers.project.create_project('test', 10, 5, 'https://google.com')
#from datetime import datetime
#join_start = datetime(2023, 7, 28, 8, 0, 0)   # Replace with your desired join start time
#join_end = datetime(2023, 7, 28, 18, 0, 0)    # Replace with your desired join end time
#event_start = datetime(2023, 8, 1, 10, 0, 0)  # Replace with your desired event start time
#event_end = datetime(2023, 8, 1, 18, 0, 0)    # Replace with your desired event end time
#helpers.phase.create_phase(join_start, join_end, event_start, event_end, p.project_id)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5052, debug=True)
