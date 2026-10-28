from api import limiter
from flask_limiter.util import get_remote_address
from . import app
from api.models import CyberEvent, User
from common.utils import retrieve_user_from_key
from flask import request, jsonify
from datetime import datetime
from api import db

@app.get('/cyber_events')
@limiter.limit("6 per minute", key_func=lambda: request.args.get("key") or get_remote_address())
def get_cyber_events():
    key = request.args.get('key')
    if not key:
        return jsonify({'error': 'API key is required'}), 401
    user = retrieve_user_from_key(key)
    if not user:
        return jsonify({'error': 'Invalid API key'}), 401
    if user.last_active:
        inactivity_period = datetime.utcnow().date() - user.last_active
        if inactivity_period.days > 180:
            user.key_displayed = True  
            db.session.commit()
            return jsonify({'error': 'Account is inactive: inactivity over 6 months. Please register again.'}), 403

    if not user.is_active():
        return jsonify({'error': 'Account is inactive. Please register again.'}), 403
    user.last_active = datetime.utcnow().date()
    db.session.commit()
    event_date = request.args.get('event_date')
    month = request.args.get('month')
    year = request.args.get('year')
    actor = request.args.get('actor')
    actor_type = request.args.get('actor_type')
    organization = request.args.get('organization')
    industry_code = request.args.get('industry_code')
    industry = request.args.get('industry')
    motive = request.args.get('motive')
    event_type = request.args.get('event_type')
    event_subtype = request.args.get('event_subtype')
    country = request.args.get('country')
    actor_country = request.args.get('actor_country')
    offset = request.args.get('offset')
    if not offset: 
        offset = 0
    try:
        offset = int(offset)
    except ValueError:
        return jsonify({'error': 'Offset must be an integer'}), 400
    result = CyberEvent.query
    if event_date: 
        result = result.filter(CyberEvent.event_date == event_date)
    if month:
        result = result.filter(CyberEvent.month == int(month))
    if year: 
        result = result.filter(CyberEvent.year == int(year))
    if actor: 
        result = result.filter(CyberEvent.actor == actor)
    if actor_type: 
        result = result.filter(CyberEvent.actor_type == actor_type)
    if organization: 
        result = result.filter(CyberEvent.organization == organization)
    if industry_code: 
        result = result.filter(CyberEvent.industry_code == int(industry_code))
    if industry: 
        result = result.filter(CyberEvent.industry == industry)
    if motive: 
        result = result.filter(CyberEvent.motive == motive)
    if event_type: 
        result = result.filter(CyberEvent.event_type == event_type)
    if event_subtype: 
        result = result.filter(CyberEvent.event_subtype == event_subtype)
    if country: 
        result = result.filter(CyberEvent.country == country)
    if actor_country: 
        result = result.filter(CyberEvent.actor_country == actor_country)
    result = result.offset(offset).limit(10)
    if result:
        response = jsonify([r.as_dict() for r in result])
        response.status_code = 200
        return response
    else:
        response = jsonify({'body': 'Not Found'})
        response.status_code = 404
        return response
@app.route('/')
def index():
    return "Cyber Events API is running"