from db import *

# Create a new Task
def create_task(task_name, task_max_points, task_type, task_start, task_end, project_id):
    task = Task(task_name=task_name, task_max_points=task_max_points, task_type=task_type, task_start=task_start, task_end=task_end, project_id=project_id)
    session.add(task)
    session.commit()
    return task

# Read all Tasks for a specific project
def get_all_tasks_for_project(project_id):
    return session.query(Task).filter_by(project_id=project_id).all()

# Read a Task by task_id
def get_task_by_id(task_id):
    return session.query(Task).filter_by(task_id=task_id).first()

# Update a Task by task_id
def update_task(task_id, task_name, task_max_points, task_type, task_start, task_end):
    task = get_task_by_id(task_id)
    if task:
        task.task_name = task_name
        task.task_max_points = task_max_points
        task.task_type = task_type
        task.task_start = task_start
        task.task_end = task_end
        session.commit()
        return task
    return None

# Delete a Task by task_id
def delete_task(task_id):
    task = get_task_by_id(task_id)
    if task:
        session.delete(task)
        session.commit()
        return True
    return False
