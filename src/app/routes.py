from flask import current_app as app
from markupsafe import escape
from app import db
import api.models
from app.forms import SignUpForm
from flask import render_template
from common.utils import generate_key, create_user
from datetime import datetime
@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index(): 
    return render_template('index.html')
@app.route('/users/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        from api.models import User
        try: 
            user = User.query.filter_by(email=form.email.data).one()
            if user.key_displayed:
                return f'<p>The email {escape(form.email.data)} is already registered and the API key has already been shown. You cannot view it again.</p>'
            else:
                user.key_displayed = True
                db.session.commit()
                return f'<p>Welcome back {escape(user.name)}</p><p><strong>Your API key is:</strong></p><h1>{user.key}</h1><p>This is the only time you will see it.</p>'
        except: 
            key = generate_key()
            create_user(email=form.email.data, name=form.name.data, creation_date=datetime.now(), key=key, key_displayed=True)
            return f'<p>Thanks for registering {escape(form.name.data)}</p><p><strong>Your API key is:</strong></p><h1>{key}</h1><p>This is the only time you will see it.</p><p>Make sure you keep your API key safe</p>'
    return render_template('signup.html', form=form)
@app.route('/test')
def test():
    return "Route is working"
@app.route('/cyber_events')
def cyber_events():
    return "Access denied", 403