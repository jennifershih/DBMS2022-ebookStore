import unittest
import json
from app import create_app, db
from app.models import User, Community, Property
from flask_jwt_extended import create_access_token

class PropertyTestCase(unittest.TestCase):
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

    def test_get_all_properties(self):
        res = self.client.get('/properties', headers={'Authorization': f'Bearer {self.user_token}'})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json(), [])

    def test_create_property(self):
        res = self.client.post('/properties', headers={'Authorization': f'Bearer {self.admin_token}'}, data=json.dumps({
            'property_id': 'C001',
            'community_id': self.community_id,
            'addr_full': 'Test Address',
            'floor_no': 1,
            'floor_total': 1,
            'building_age': 1,
            'total_area_ping': 1.0,
            'main_use': 'Test Use',
            'building_type': 'Test Type'
        }), content_type='application/json')
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.get_json()['property_id'], 'C001')

    def test_get_property(self):
        prop = Property(property_id='C001', community_id=self.community_id, addr_full='Test Address')
        with self.app.app_context():
            db.session.add(prop)
            db.session.commit()
        
        res = self.client.get(f'/properties/C001', headers={'Authorization': f'Bearer {self.user_token}'})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()['addr_full'], 'Test Address')

if __name__ == '__main__':
    unittest.main()
