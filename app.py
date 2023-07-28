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


"""
end point: " /chGeneral "

Server waiting ==>

{
    "id": 1,
    "title": "Project title",
    "max_team_num": 5,
    "num_of_members": 3,
}
"""

@app.route('/chGeneral', methods=['POST'])
def change_general():
    project = request.get_json()
    if project is not None:
        try:
            project_id = int(project['id'])
            #kellene egy adatbázis lekérdezés, hogy megkapjuk a projekt adatait a project_id alapján
            project = helpers.project.get_project_by_id(project_id)
            if project is not None:
                project.name = project['title']
                project.max_team_num = project['max_team_num']
                project.num_of_members = project['num_of_members']
                helpers.project.update_project(project_id=project_id, name=project.name, max_team_num=project.max_team_num, num_of_members=project.num_of_members)
                return jsonify({"message": "Project updated"}), 200,
            else:
                return jsonify({"error": "Project ID not found"}), 404
        except ValueError:
            return jsonify({"error": "Invalid Project ID"}), 400

@app.route('/getGeneral', methods=['GET'])
def get_general():
    project_id = request.args.get('id')
    if project_id is not None:
        try:
            project_id = int(project_id)
            #kellene egy adatbázis lekérdezés, hogy megkapjuk a projekt adatait a project_id alapján
            project = helpers.project.get_project_by_id(project_id)
            if project is not None:
                return jsonify({
                    "id": project_id,
                    "name": project.name,
                    "max_team_num": project.max_team_num,
                    "num_of_members": project.num_of_members,
                }), 200
            else:
                return jsonify({"error": "Project ID not found"}), 404
        except ValueError:
            return jsonify({"error": "Invalid Project ID"}), 400

@app.route('/getJoining', methods=['GET'])
def get_joining():
    project_id = request.args.get('id')
    if project_id is not None:
        try:
            project_id = int(project_id)
            #kellene egy adatbázis lekérdezés, hogy megkapjuk a projekt adatait a project_id alapján
            project = helpers.project.get_project_by_id(project_id)
            if project is not None:
                joining_page = helpers.joining.get_joining_page_for_project(project_id)
                if joining_page is not None:
                    return jsonify({
                        "title": joining_page.title,
                        "body": joining_page.body,
                        "footer": joining_page.footer,
                    }), 200
                else:
                    return jsonify({"error": "Page not found"}), 404
            else:
                return jsonify({"error": "Project ID not found"}), 404
        except ValueError:
            return jsonify({"error": "Invalid Project ID"}), 400
    else:
        return jsonify({"error": "Project ID parameter is missing"}), 400

@app.route('/chJoining', methods=['POST'])
def change_joining():
    page = request.get_json()
    if page is not None:
        try:
            project_id = int(page['id'])
            #kellene egy adatbázis lekérdezés, hogy megkapjuk a projekt adatait a project_id alapján
            project = helpers.project.get_project_by_id(project_id)
            if project is not None:
                #kellene egy adatbázis lekérdezés, hogy megkapjuk a projekt csatlakozási oldalát a project_id alapján
                joining_page = helpers.joining.get_joining_page_for_project(project_id)
                if joining_page is not None:
                    joining_page.title = page['title']
                    joining_page.body = page['body']
                    joining_page.footer = page['footer']
                    helpers.joining.update_joining_page(joining_id=joining_page.joining_id, title=joining_page.title, body=joining_page.body, footer=joining_page.footer)
                    return jsonify({"message": "Page updated"}), 200,
                else:
                    return jsonify({"error": "Page not found"}), 404
            else:
                return jsonify({"error": "Project ID not found"}), 404
        except ValueError:
            return jsonify({"error": "Invalid Project ID"}), 400


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

@app.route('/getDesign/<project_id>', methods=['GET'])
def get_design(project_id):
    design = helpers.design.get_design_by_project_id(project_id)    
    teams = helpers.team.get_all_teams_in_project(project_id)
    teams_parsed = []
    for team in teams:
        teams_parsed.append({
            'team_name': team.team_name,
            'id': team.team_id,
            'color': team.color
        })
    parsed = {
            'header': design.header_text,
            'bg_img': design.bg_img_url,
            'color1': design.base_color1,
            'color2': design.base_color2,
            'color3': design.base_color3,
            'teams': teams_parsed
        }
    
    return jsonify(parsed)

@app.route('/chDesign', methods=['POST'])
def change_design():
    data = request.get_json()
    design = helpers.design.update_design(helpers.design.get_design_for_project(data.get('project_id')), data.get('header'), data.get('bg_img'), data.get('color1'), data.get('color2'), data.get('color3'))
    if not design:
        return "Design update failed"
    return {
            'header': design.header_text,
            'bg_img': design.bg_img_url,
            'color1': design.base_color1,
            'color2': design.base_color2,
            'color3': design.base_color3,
        }

#p = helpers.project.create_project('test', 10, 5, 'https://google.com')
#from datetime import datetime
#join_start = datetime(2023, 7, 28, 8, 0, 0)   # Replace with your desired join start time
#join_end = datetime(2023, 7, 28, 18, 0, 0)    # Replace with your desired join end time
#event_start = datetime(2023, 8, 1, 10, 0, 0)  # Replace with your desired event start time
#event_end = datetime(2023, 8, 1, 18, 0, 0)    # Replace with your desired event end time
#helpers.phase.create_phase(join_start, join_end, event_start, event_end, p.project_id)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5052, debug=True)


