import unittest
import json
from app import create_app, db
from app.models import User, Community, Property, Transaction
from flask_jwt_extended import create_access_token
from datetime import date

class TransactionTestCase(unittest.TestCase):
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

            prop = Property(property_id='C001', community_id=self.community_id, addr_full='Test Address')
            db.session.add(prop)
            db.session.commit()
            self.property_id = prop.property_id

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_all_transactions(self):
        res = self.client.get('/transactions', headers={'Authorization': f'Bearer {self.user_token}'})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json(), [])

    def test_create_transaction(self):
        res = self.client.post('/transactions', headers={'Authorization': f'Bearer {self.admin_token}'}, data=json.dumps({
            'property_id': self.property_id,
            'transaction_date': '2023-01-01',
            'total_price_10k': 1000,
            'unit_price_10k_per_ping': 32.8
        }), content_type='application/json')
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.get_json()['total_price_10k'], 1000)

if __name__ == '__main__':
    unittest.main()
