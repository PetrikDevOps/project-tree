import importlib
import os

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_session import Session
from werkzeug.middleware.proxy_fix import ProxyFix

import config
import helpers

from helpers.project import get_project_by_id

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

@app.route('/getPhase', methods=['GET'])
def get_phase():
    project_id = request.args.get('id')
    if project_id is not None:
        try:
            project_id = int(project_id)
            #kellene egy adatbázis lekérdezés, hogy megkapjuk a projekt adatait a project_id alapján
            project = get_project_by_id(project_id)
            if project_id == dummy_data["id"]:
                return jsonify(dummy_data)
            else:
                return jsonify({"error": "Project ID not found"}), 404
        except ValueError:
            return jsonify({"error": "Invalid Project ID"}), 400
    else:
        return jsonify({"error": "Project ID parameter is missing"}), 400


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5052, debug=True)


