from db import *

def create_design(header_text, bg_img_url, base_color1, base_color2, base_color3, team_color1, team_color2, team_color3, project_id):
    design = Design(
        header_text=header_text,
        bg_img_url=bg_img_url,
        base_color1=base_color1,
        base_color2=base_color2,
        base_color3=base_color3,
        team_color1=team_color1,
        team_color2=team_color2,
        team_color3=team_color3,
        project_id=project_id
    )
    session.add(design)
    session.commit()
    return design

def get_all_designs():
    return session.query(Design).all()

def get_design_by_id(design_id):
    return session.query(Design).filter_by(design_id=design_id).first()

def get_design_for_project(project_id):
    return session.query(Design).filter_by(project_id=project_id).first()

def update_design(design_id, header_text, bg_img_url, base_color1, base_color2, base_color3, team_color1, team_color2, team_color3):
    design = get_design_by_id(design_id)
    if design:
        design.header_text = header_text
        design.bg_img_url = bg_img_url
        design.base_color1 = base_color1
        design.base_color2 = base_color2
        design.base_color3 = base_color3
        design.team_color1 = team_color1
        design.team_color2 = team_color2
        design.team_color3 = team_color3
        session.commit()
        return True
    return False

def delete_design(design_id):
    design = get_design_by_id(design_id)
    if design:
        session.delete(design)
        session.commit()
        return True
    return False
