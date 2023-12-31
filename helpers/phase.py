from db import *
from datetime import datetime
from helpers.project import get_project_by_id

def create_phase(join_start, join_end, event_start, event_end, project_id):
    phase = Phase(join_start=join_start, join_end=join_end, event_start=event_start, event_end=event_end, project_id=project_id)
    session.add(phase)
    session.commit()
    return phase

def get_phase_by_id(phase_id):
    return session.query(Phase).filter_by(phase_id=phase_id).first()

def get_phase_for_project(project_id):
    return session.query(Phase).filter_by(project_id=project_id).first()

def get_current_phase(project_id):
    now = datetime.now()
    phase = get_phase_for_project(project_id)
    js, je, es, ee = phase.join_start, phase.join_end, phase.event_start, phase.event_end

    if js <= now <= je:
        return 'joining'
    elif es <= now <= ee:
        return 'event'
    else:
        return None

def update_phase(phase_id=None, join_start=None, join_end=None, event_start=None, event_end=None):
    phase = get_phase_by_id(phase_id) if phase_id is not None else None
    if phase:
        phase.join_start = join_start if join_start is not None else phase.join_start
        phase.join_end = join_end if join_end is not None else phase.join_end
        phase.event_start = event_start if event_start is not None else phase.event_start
        phase.event_end = event_end if event_end is not None else phase.event_end
        session.commit()
        return phase
    return None


def delete_phase(phase_id):
    phase = get_phase_by_id(phase_id)
    if phase:
        session.delete(phase)
        session.commit()
        return True
    return False
