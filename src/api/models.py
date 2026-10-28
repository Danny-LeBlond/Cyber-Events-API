
from app import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False)
    key = db.Column(db.String, nullable=False)
    key_displayed = db.Column(db.Boolean, default=False)
    last_active = db.Column(db.Date)

    def is_active(self):
        return self.key_displayed is True

class CyberEvent(db.Model):
    __tablename__ = 'cyber_events'
    id = db.Column(db.String, primary_key=True)
    date = db.Column(db.Date)
    year = db.Column(db.Integer)
    month = db.Column(db.Integer)
    actor = db.Column(db.String)
    motive = db.Column(db.String)
    victim = db.Column(db.String)
    records_lost = db.Column(db.Integer)
    sector = db.Column(db.String)
    type_of_incident = db.Column(db.String)
    action = db.Column(db.String)
    action_detail = db.Column(db.String)
    summary = db.Column(db.Text)
    source_link = db.Column(db.String)
    country = db.Column(db.String)
    state = db.Column(db.String)
