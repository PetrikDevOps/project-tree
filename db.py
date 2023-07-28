import uuid
from sqlalchemy import create_engine, Column, String, Integer, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///db/project-tree.db')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    user_id = Column(String(36), primary_key=True, default=str(uuid.uuid4))
    name = Column(String)
    grade = Column(String)
    is_admin = Column(Boolean, default=False)

class Project(Base):
    __tablename__ = 'projects'

    project_id = Column(String(36), primary_key=True, default=str(uuid.uuid4))
    name = Column(String)
    leaderboard_url = Column(String)
    num_of_groups = Column(Integer)
    num_of_members = Column(Integer)
    teams = relationship('Team', back_populates='project')
    phases = relationship('Phase', back_populates='project')
    design = relationship('Design', uselist=False, back_populates='project')

class Team(Base):
    __tablename__ = 'teams'

    team_id = Column(String(36), primary_key=True, default=str(uuid.uuid4))
    team_name = Column(String)
    color = Column(String)
    project_id = Column(String(36), ForeignKey('projects.project_id'))
    project = relationship('Project', back_populates='teams')
    team_members = relationship('User', secondary='team_memberships')

team_memberships = Table('team_memberships', Base.metadata,
    Column('team_id', String(36), ForeignKey('teams.team_id')),
    Column('user_id', String(36), ForeignKey('users.user_id'))
)

class Phase(Base):
    __tablename__ = 'phases'

    phase_id = Column(String(36), primary_key=True, default=str(uuid.uuid4))
    join_start = Column(DateTime)
    join_end = Column(DateTime)
    event_start = Column(DateTime)
    event_end = Column(DateTime)
    project_id = Column(String(36), ForeignKey('projects.project_id'))
    project = relationship('Project', back_populates='phases')

class Design(Base):
    __tablename__ = 'designs'

    design_id = Column(String(36), primary_key=True, default=str(uuid.uuid4))
    header_text = Column(String)
    bg_img_url = Column(String)
    base_color1 = Column(String)
    base_color2 = Column(String)
    base_color3 = Column(String)
    member_count = Column(Integer, default=0)
    project_id = Column(String(36), ForeignKey('projects.project_id'))
    project = relationship('Project', back_populates='design')

class JoiningPage(Base):
    __tablename__ = 'joining_pages'

    page_id = Column(String(36), primary_key=True, default=str(uuid.uuid4))
    page_title = Column(String)
    page_body = Column(String)
    page_footer = Column(String)
    project_id = Column(String(36), ForeignKey('projects.project_id'))
    project = relationship('Project', back_populates='phases')

class Task(Base):
    __tablename__ = 'tasks'

    task_id = Column(String(36), primary_key=True, default=str(uuid.uuid4))
    task_name = Column(String)
    task_max_points = Column(Integer)
    task_type = Column(Integer)
    task_start = Column(DateTime)
    task_end = Column(DateTime)
    project_id = Column(String(36), ForeignKey('projects.project_id'))
    project = relationship('Project', back_populates='phases')

class Points(Base):
    __tablename__ = 'points'


    points_id = Column(String(36), primary_key=True, default=str(uuid.uuid4))
    task_id = Column(String(36), ForeignKey('tasks.task_id'))
    team_id = Column(String(36), ForeignKey('teams.team_id'))
    points = Column(Integer)

    project_id = Column(String(36), ForeignKey('projects.project_id'))
    project = relationship('Project', back_populates='phases')


# Update the relationships in the Project and User models
Project.phases = relationship('Phase', back_populates='project')
Project.design = relationship('Design', uselist=False, back_populates='project')

# Create the tables in the database
Base.metadata.create_all(engine)
