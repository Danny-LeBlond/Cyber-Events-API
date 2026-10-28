import flask
from flask import request
from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'common')))
app = Flask("Cyber Events Web API")
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:135791@localhost:5432/cyber_events'
from api.models import db
db.init_app(app)
import redis
try:
    test_redis = redis.Redis()
    test_redis.set("limiter_test_key", "value", ex=10)
except Exception as e:
    pass
limiter = Limiter(
    key_func=lambda: request.args.get("key") or get_remote_address(),
    storage_uri="redis://localhost:6379",
    default_limits=[]
)
limiter.init_app(app)
from api import routes
import api.models
if __name__ == "__main__":
    app.run(port=5001, debug=True)
