import unittest
from datetime import datetime, timedelta
from app import create_app, db
from common.utils import create_user
class WhiteBoxTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()
    def test_inactive_user_blocked(self):
        with self.app.app_context():
            from api.models import User
            existing_user = User.query.filter_by(email="whiteboxtest@example.com").first()
            if existing_user:
                db.session.delete(existing_user)
                db.session.commit()
            stale_date = datetime.now() - timedelta(days=190)
            create_user(
                email="whiteboxtest@example.com",
                name="WhiteBox Tester",
                creation_date=datetime.now(),
                key="testinactivekey123",
                key_displayed=True
            )
            user = User.query.filter_by(email="whiteboxtest@example.com").first()
            user.last_active = stale_date
            db.session.commit()
            response = self.client.get('/cyber_events?api_key=testinactivekey123')
            self.assertEqual(response.status_code, 403)
            self.assertIn("access denied", response.get_data(as_text=True).lower())
if __name__ == '__main__':
    unittest.main()