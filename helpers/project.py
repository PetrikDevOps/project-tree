from db import *

def create_project(name, num_of_groups, num_of_members, leaderboard_url):
    project = Project(name=name, num_of_groups=num_of_groups, num_of_members=num_of_members, leaderboard_url=leaderboard_url)
    session.add(project)
    session.commit()
    return project

def get_all_projects():
    return session.query(Project).all()

def get_project_by_id(project_id):
    return session.query(Project).filter_by(project_id=project_id).first()

def update_project(project_id, project_name):
    project = get_project_by_id(project_id)
    if project:
        project.project_name = project_name
        session.commit()
        return project
    return None

def delete_project(project_id):
    project = get_project_by_id(project_id)
    if project:
        session.delete(project)
        session.commit()
        return True
    return False
