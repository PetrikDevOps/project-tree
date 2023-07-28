from db import *

# Create a new JoiningPage
def create_joining_page(page_title, page_body, page_footer, project_id):
    joining_page = JoiningPage(page_title=page_title, page_body=page_body, page_footer=page_footer, project_id=project_id)
    session.add(joining_page)
    session.commit()
    return joining_page

# Read all JoiningPages for a specific project
def get_all_joining_page_for_project(project_id):
    return session.query(JoiningPage).filter_by(project_id=project_id).first()

# Read a JoiningPage by page_id
def get_joining_page_by_id(page_id):
    return session.query(JoiningPage).filter_by(page_id=page_id).first()

# Update a JoiningPage by page_id
def update_joining_page(page_id, page_title, page_body, page_footer):
    joining_page = get_joining_page_by_id(page_id)
    if joining_page:
        joining_page.page_title = page_title
        joining_page.page_body = page_body
        joining_page.page_footer = page_footer
        session.commit()
        return True
    return False

# Delete a JoiningPage by page_id
def delete_joining_page(page_id):
    joining_page = get_joining_page_by_id(page_id)
    if joining_page:
        session.delete(joining_page)
        session.commit()
        return True
    return False
