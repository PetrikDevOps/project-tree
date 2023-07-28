from helpers.team import get_team_by_id
from db import *

def create_user(name, grade, is_admin=False):
    user = User(name=name, grade=grade, is_admin=is_admin)
    session.add(user)
    session.commit()
    return user

def get_all_users():
    return session.query(User).all()

def get_user_by_id(user_id):
    return session.query(User).filter_by(user_id=user_id).first()

def get_users_by_team(team_id):
    team = get_team_by_id(team_id)
    
    if team:
        return team.team_members
    return None

def update_user(user_id, name, grade, is_admin):
    user = get_user_by_id(user_id)
    if user:
        user.name = name
        user.grade = grade
        user.is_admin = is_admin
        session.commit()
        return user
    return None

def delete_user(user_id):
    user = get_user_by_id(user_id)
    if user:
        session.delete(user)
        session.commit()
        return True
    return False


def add_user_to_team(user_id, team_id):
    user = get_user_by_id(user_id)
    team = get_team_by_id(team_id)
    
    if user and team:
        team.team_members.append(user)
        session.commit()
        return True
    return False

# Remove a user from a team
def remove_user_from_team(user_id, team_id):
    user = get_user_by_id(user_id)
    team = get_team_by_id(team_id)
    
    if user and team and user in team.team_members:
        team.team_members.remove(user)
        session.commit()
        return True
    return False
