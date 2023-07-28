from db import *

def create_team(team_name, project_id):
    team = Team(team_name=team_name, project_id=project_id)
    session.add(team)
    session.commit()
    return team

# Read all teams
def get_all_teams():
    return session.query(Team).all()

# Read a team by team_id
def get_team_by_id(team_id):
    return session.query(Team).filter_by(team_id=team_id).first()

# Update a team by team_id
def update_team(team_id, team_name):
    team = get_team_by_id(team_id)
    if team:
        team.team_name = team_name
        session.commit()
        return True
    return False

# Delete a team by team_id
def delete_team(team_id):
    team = get_team_by_id(team_id)
    if team:
        session.delete(team)
        session.commit()
        return True
    return False
