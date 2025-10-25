import unittest
import json
from app import create_app, db
from app.models import User, Community
from flask_jwt_extended import create_access_token

class CommunityTestCase(unittest.TestCase):
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

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_all_communities(self):
        res = self.client.get('/communities', headers={'Authorization': f'Bearer {self.user_token}'})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json(), [])

    def test_create_community(self):
        res = self.client.post('/communities', headers={'Authorization': f'Bearer {self.admin_token}'}, data=json.dumps({
            'district_name': 'Test District',
            'community_name': 'Test Community'
        }), content_type='application/json')
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.get_json()['district_name'], 'Test District')

    def test_create_community_as_user(self):
        res = self.client.post('/communities', headers={'Authorization': f'Bearer {self.user_token}'}, data=json.dumps({
            'district_name': 'Test District',
            'community_name': 'Test Community'
        }), content_type='application/json')
        self.assertEqual(res.status_code, 403)

    def test_get_community(self):
        community = Community(district_name='Test District', community_name='Test Community')
        with self.app.app_context():
            db.session.add(community)
            db.session.commit()
            community_id = community.community_id
        
        res = self.client.get(f'/communities/{community_id}', headers={'Authorization': f'Bearer {self.user_token}'})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()['community_name'], 'Test Community')

    def test_update_community(self):
        community = Community(district_name='Test District', community_name='Test Community')
        with self.app.app_context():
            db.session.add(community)
            db.session.commit()
            community_id = community.community_id

        res = self.client.put(f'/communities/{community_id}', headers={'Authorization': f'Bearer {self.admin_token}'}, data=json.dumps({
            'district_name': 'Updated District',
            'community_name': 'Updated Community'
        }), content_type='application/json')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()['district_name'], 'Updated District')

    def test_delete_community(self):
        community = Community(district_name='Test District', community_name='Test Community')
        with self.app.app_context():
            db.session.add(community)
            db.session.commit()
            community_id = community.community_id

        res = self.client.delete(f'/communities/{community_id}', headers={'Authorization': f'Bearer {self.admin_token}'})
        self.assertEqual(res.status_code, 204)

if __name__ == '__main__':
    unittest.main()
