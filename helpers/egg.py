from db import *
from sqlalchemy.orm.exc import NoResultFound
import qrcode
import io

# Function to create a new egg
def create_egg(name, project_id, valid_from, valid_until, riddle):
    new_egg = Egg(name=name, project_id=project_id, valid_from=valid_from, valid_until=valid_until, riddle=riddle)
    session.add(new_egg)
    session.commit()
    return new_egg

def get_all_eggs():
    return session.query(Egg).all()

# Function to read (retrieve) an egg by its ID
def get_egg_by_id(egg_id):
    try:
        return session.query(Egg).filter_by(egg_id=egg_id).one()
    except NoResultFound:
        return None

# Function to update an existing egg's name
def update_egg_riddle(egg_id, new_name):
    egg = get_egg_by_id(session, egg_id)
    if egg:
        egg.riddle = new_name
        session.commit()
        return egg
    return None

def check_egg_valid(egg):
    if egg.valid_until and egg.valid_until < datetime.now():
        return True
    return False

def team_found_egg(team_id, egg_id):
    team = session.query(Team).get(team_id)
    egg = session.query(Egg).get(egg_id)

    team.found_eggs.append(egg)
    session.commit()
    return True

def create_qr_img(egg_id):
    if not get_egg_by_id(egg_id):
        return None
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(egg_id)
    qr.make(fit=True)

    img_byte_stream = io.BytesIO()

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(img_byte_stream, format='PNG')

    img_byte_stream.seek(0)

    return img_byte_stream
