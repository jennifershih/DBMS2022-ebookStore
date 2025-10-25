import unittest
import json
from app import create_app, db
from app.models import User, Community, Transportation
from flask_jwt_extended import create_access_token

class TransportationTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            admin_user = User(username='admin', role='admin')
            admin_user.set_password('admin')
            db.session.add(admin_user)
            db.session.commit()
            self.admin_token = create_access_token(identity=str(admin_user.id))

            user = User(username='user', role='user')
            user.set_password('user')
            db.session.add(user)
            db.session.commit()
            self.user_token = create_access_token(identity=str(user.id))

            community = Community(district_name='Test District', community_name='Test Community')
            db.session.add(community)
            db.session.commit()
            self.community_id = community.community_id

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_all_transportations(self):
        res = self.client.get('/transportations', headers={'Authorization': f'Bearer {self.user_token}'})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json(), [])

    def test_create_transportation(self):
        res = self.client.post('/transportations', headers={'Authorization': f'Bearer {self.admin_token}'}, data=json.dumps({
            'transport_id': 'T001',
            'community_id': self.community_id,
            'type': 'Test Type',
            'name': 'Test Name',
            'line_name': 'Test Line',
            'station_code': 'T1',
            'latitude': 25.0,
            'longitude': 121.0
        }), content_type='application/json')
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.get_json()['name'], 'Test Name')

if __name__ == '__main__':
    unittest.main()
