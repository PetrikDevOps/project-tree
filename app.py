import importlib
import os

from flask import Flask, render_template, jsonify, request, session, send_file
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

@app.route('/chPhase', methods=['POST'])
def change_phase():
    phase = request.get_json()
    if phase is not None:
        try:
            project_id = int(phase['id'])
            #kellene egy adatbázis lekérdezés, hogy megkapjuk a projekt adatait a project_id alapján
            project = helpers.project.get_project_by_id(project_id)
            if project is not None:
                #kellene egy adatbázis lekérdezés, hogy megkapjuk a projekt fázisát a project_id alapján
                phase = helpers.phase.get_phase_for_project(project_id)
                if phase is not None:
                    phase.join_start = phase['join_start']
                    phase.join_end = phase['join_end']
                    phase.event_start = phase['event_start']
                    phase.event_end = phase['event_end']
                    helpers.phase.update_phase(phase_id=phase.phase_id, join_start=phase.join_start, join_end=phase.join_end, event_start=phase.event_start, event_end=phase.event_end)
                    return jsonify({"message": "Phase updated"}), 200,
                else:
                    return jsonify({"error": "Phase not found"}), 404
            else:
                return jsonify({"error": "Project ID not found"}), 404
        except ValueError:
            return jsonify({"error": "Invalid Project ID"}), 400


@app.route('/getPhase', methods=['GET'])
def get_phase():
    project_id = request.args.get('id')
    if project_id is not None:
        try:
            project_id = int(project_id)
            #kellene egy adatbázis lekérdezés, hogy megkapjuk a projekt adatait a project_id alapján
            project = helpers.project.get_project_by_id(project_id)
            if project is not None:
                phase = helpers.project.get_phase_for_project(project_id)
    
                return jsonify({
                    "id": project_id,
                    "join_start": phase.join_start,
                    "join_end": phase.join_end,
                    "event_start": phase.event_start,
                    "event_end": phase.event_end,
                }), 200
            else:
                return jsonify({"error": "Project ID not found"}), 404
        except ValueError:
            return jsonify({"error": "Invalid Project ID"}), 400
    else:
        return jsonify({"error": "Project ID parameter is missing"}), 400

@app.route('/getProjectStats', methods=['GET'])
def get_projects():
    parsed = []
    for project in helpers.project.get_all_projects():
        top3 = helpers.leaderboard.get_top3(project.project_id)
        project_data = {
            'project_id': project.project_id,
            'name': project.name,
            'state': helpers.phase.get_current_phase(project.project_id),
            'max_team_num': project.max_team_num,
            'current_team_num': len(project.teams),
            'first': top3[0].team_name if len(top3) > 0 else None,
            'second': top3[1].team_name if len(top3) > 1 else None,
            'third': top3[2].team_name if len(top3) > 2 else None,
        }
        parsed.append(project_data)
    return jsonify({'projects': parsed})


@app.route('/getAllEggs', methods=['GET'])
def get_eggs():
    parsed = []
    for egg in helpers.egg.get_all_eggs():
        egg_data = {
            'egg_id': egg.egg_id,
            'egg_name': egg.egg_name,
            'project_id': egg.project_id,
            'riddle': egg.riddle,
            'valid_until': egg.valid_until,
        }
        parsed.append(egg_data)
    return jsonify({'eggs': parsed})


@app.route('/egg/<egg_id>', methods=['GET', 'POST'])
def get_egg(egg_id):
    if request.method == 'GET':
        return "nem"
    elif request.method == 'POST':
        data = request.get_json()
        team = helpers.team.get_team_by_val_code(data.get('val_code'))
        if not team:
            return "Code error"
        if not helpers.egg.check_egg_valid(egg_id):
            return "Egg not valid"
        helpers.egg.team_found_egg(team.team_id, egg_id)


@app.route('/chEgg', methods=['POST'])
def change_egg():
    data = request.get_json()
    oegg = helpers.egg.get_egg_by_id(data.get('egg_id'))
    if not oegg:
        return "Egg not found"
    
    egg = helpers.egg.update_egg_riddle(oegg.egg_id, data.get('riddle'))
    if not egg:
        return "Riddle update failed"
    return {
            'egg_id': egg.egg_id,
            'egg_name': egg.egg_name,
            'project_id': egg.project_id,
            'riddle': egg.riddle,
            'valid_until': egg.valid_until,}


@app.route('/genEggQR/<egg_id>', methods=['GET'])
def get_egg_qr(egg_id):
    img = helpers.egg.create_qr_img(egg_id)
    if not img:
        return "Not a valid egg id"
    return send_file(img, mimetype='image/png')





#p = helpers.project.create_project('test', 10, 5, 'https://google.com')
#from datetime import datetime
#join_start = datetime(2023, 7, 28, 8, 0, 0)   # Replace with your desired join start time
#join_end = datetime(2023, 7, 28, 18, 0, 0)    # Replace with your desired join end time
#event_start = datetime(2023, 8, 1, 10, 0, 0)  # Replace with your desired event start time
#event_end = datetime(2023, 8, 1, 18, 0, 0)    # Replace with your desired event end time
#helpers.phase.create_phase(join_start, join_end, event_start, event_end, p.project_id)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5052, debug=True)


