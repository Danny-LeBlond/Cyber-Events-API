import os
import secrets
import string
from flask import current_app
def get_db():
    return current_app.extensions['sqlalchemy']
def generate_key(length=32):
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))
def create_user(email='', name='', creation_date='01/01/1900', key=generate_key(), key_displayed=False):
    from api.models import User
    db = get_db()
    user = User(
        email=email,
        name=name,
        creation_date=creation_date,
        key=key,
        key_displayed=key_displayed)
    db.session.add(user)
    db.session.commit()
def delete_user(email): 
    from api.models import User
    db = get_db()
    user = User.query.filter_by(email=email).one()
    db.session.delete(user)
    db.session.commit()
def retrieve_user_from_email(email): 
    from api.models import User
    db = get_db()
    user = User.query.filter_by(email=email).one()
    return user
def retrieve_user_from_key(key):
    from api.models import User
    db = get_db()
    user = User.query.filter_by(key=key).first()
    return user
