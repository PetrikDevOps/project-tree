import random
import uuid

from datetime import datetime
from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer, String,
                        Table, create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

engine = create_engine('sqlite:///db/project-tree.db')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    user_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String)
    grade = Column(String)
    is_admin = Column(Boolean, default=False)

class Project(Base):
    __tablename__ = 'projects'

    project_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String)
    leaderboard_url = Column(String)
    max_team_num = Column(Integer)
    num_of_members = Column(Integer)
    teams = relationship('Team', back_populates='project')
    phases = relationship('Phase', back_populates='project')
    design = relationship('Design', uselist=False, back_populates='project')
    joining_page = relationship('JoiningPage', uselist=False, back_populates='project')
    tasks = relationship('Task', back_populates='project')
    eggs = relationship('Egg', back_populates='project')

class Team(Base):
    __tablename__ = 'teams'

    team_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    team_name = Column(String)
    color = Column(String)
    project_id = Column(String(36), ForeignKey('projects.project_id'))
    project = relationship('Project', back_populates='teams')
    team_members = relationship('User', secondary='team_memberships')
    validation_code = Column(String, default=lambda: str(random.randint(10000,99999)))
    found_eggs = relationship('Egg', secondary='egg_teamships', back_populates='found_by_teams')

team_memberships = Table('team_memberships', Base.metadata,
    Column('team_id', String(36), ForeignKey('teams.team_id')),
    Column('user_id', String(36), ForeignKey('users.user_id'))
)

class Phase(Base):
    __tablename__ = 'phases'

    phase_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    join_start = Column(DateTime)
    join_end = Column(DateTime)
    event_start = Column(DateTime)
    event_end = Column(DateTime)
    project_id = Column(String(36), ForeignKey('projects.project_id'))
    project = relationship('Project', back_populates='phases')

class Design(Base):
    __tablename__ = 'designs'

    design_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    header_text = Column(String)
    bg_img_url = Column(String)
    base_color1 = Column(String)
    base_color2 = Column(String)
    base_color3 = Column(String)
    member_count = Column(Integer, default=0)
    project_id = Column(String(36), ForeignKey('projects.project_id'))
    project = relationship('Project', back_populates='design')

class Egg(Base):
    __tablename__ = 'eastereggs'

    egg_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String)
    riddle = Column(String)
    project_id = Column(String(36), ForeignKey('projects.project_id'))
    project = relationship('Project', back_populates='eggs')
    found_by_teams = relationship('Team', secondary='egg_teamships')
    valid_from = Column(DateTime)
    valid_until = Column(DateTime)

egg_teamships = Table('egg_teamships', Base.metadata,
    Column('egg_id', String(36), ForeignKey('eastereggs.egg_id')),
    Column('team_id', String(36), ForeignKey('teams.team_id'))
)


class JoiningPage(Base):
    __tablename__ = 'joining_pages'

    page_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    page_title = Column(String)
    page_body = Column(String)
    page_footer = Column(String)
    project_id = Column(String(36), ForeignKey('projects.project_id'))
    project = relationship('Project', back_populates='joining_page')

class Task(Base):
    __tablename__ = 'tasks'

    task_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    task_name = Column(String)
    task_max_points = Column(Integer)
    task_type = Column(Integer)
    task_start = Column(DateTime)
    task_end = Column(DateTime)
    project_id = Column(String(36), ForeignKey('projects.project_id'))
    project = relationship('Project', back_populates='tasks')
    points = relationship('Points', back_populates='task')

class Points(Base):
    __tablename__ = 'points'

    points_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    task_id = Column(String(36), ForeignKey('tasks.task_id'))
    team_id = Column(String(36), ForeignKey('teams.team_id'))
    points = Column(Integer)

    task = relationship('Task', back_populates='points')

# Create the tables in the database
Base.metadata.create_all(engine)
