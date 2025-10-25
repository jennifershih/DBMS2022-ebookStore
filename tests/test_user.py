import unittest
import json
from app import create_app, db
from app.models import User

class UserTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_register(self):
        res = self.client.post('/register', data=json.dumps({
            'username': 'test',
            'password': 'test'
        }), content_type='application/json')
        self.assertEqual(res.status_code, 201)

    def test_login(self):
        user = User(username='test', role='user')
        user.set_password('test')
        with self.app.app_context():
            db.session.add(user)
            db.session.commit()

        res = self.client.post('/login', data=json.dumps({
            'username': 'test',
            'password': 'test'
        }), content_type='application/json')
        self.assertEqual(res.status_code, 200)
        self.assertIn('access_token', res.get_json())

if __name__ == '__main__':
    unittest.main()
