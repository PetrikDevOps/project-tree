from db import *
from sqlalchemy import func

# Create Points for a specific Task and Team
def create_points(task_id, team_id, points, project_id):
    points_record = Points(task_id=task_id, team_id=team_id, points=points, project_id=project_id)
    session.add(points_record)
    session.commit()
    return points_record

# Read all Points for a specific project
def get_all_points_for_team(team_id):
    return session.query(Points).filter_by(team_id=team_id).all()

# Read Points for a specific Task and Team
def get_points_by_task_and_team(task_id, team_id):
    return session.query(Points).filter_by(task_id=task_id, team_id=team_id).first()

# Update Points for a specific Task and Team
def update_points(task_id, team_id, points):
    points_record = get_points_by_task_and_team(task_id, team_id)
    if points_record:
        points_record.points = points
        session.commit()
        return points_record
    return None

# Delete Points for a specific Task and Team
def delete_points(task_id, team_id):
    points_record = get_points_by_task_and_team(task_id, team_id)
    if points_record:
        session.delete(points_record)
        session.commit()
        return True
    return False

def get_team_total_points(team_id):
    team_points = session.query(func.sum(Points.points)).filter_by(team_id=team_id).scalar()

    if team_points is None:
        return 0
    else:
        return team_points
    
def get_top_3_teams(project_id):
    return session.query(Team.team_id, Team.team_name, func.sum(Points.points).label('total_points')) \
            .join(Points, Team.team_id == Points.team_id) \
            .filter(Team.project_id == project_id) \
            .group_by(Team.team_id, Team.team_name) \
            .order_by(func.sum(Points.points).desc()) \
            .limit(3) \
            .all()

