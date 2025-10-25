import unittest
import json
from app import create_app, db
from app.models import User, Community, Property, Transaction, QuickSearch
from flask_jwt_extended import create_access_token

class QuickSearchTestCase(unittest.TestCase):
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

            community1 = Community(district_name='屏東縣屏東市', community_name='Test Community 1')
            community2 = Community(district_name='台南市新市區', community_name='Test Community 2')
            community3 = Community(district_name='高雄市路竹區', community_name='Test Community 3')
            db.session.add_all([community1, community2, community3])
            db.session.commit()

            prop1 = Property(property_id='P001', community_id=community1.community_id, addr_full='Test Address 1')
            prop2 = Property(property_id='P002', community_id=community2.community_id, addr_full='Test Address 2')
            prop3 = Property(property_id='P003', community_id=community3.community_id, addr_full='Test Address 3')
            db.session.add_all([prop1, prop2, prop3])
            db.session.commit()

            trans1 = Transaction(property_id='P001', transaction_date='2023-01-01', total_price_10k=1000)
            trans2 = Transaction(property_id='P002', transaction_date='2023-01-02', total_price_10k=2000)
            trans3 = Transaction(property_id='P003', transaction_date='2023-01-03', total_price_10k=3000)
            db.session.add_all([trans1, trans2, trans3])
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_quick_search(self):
        res = self.client.post('/quick_search', headers={'Authorization': f'Bearer {self.admin_token}'}, data=json.dumps({
            'name': '南部科學園區',
            'query': {
                'locations': [
                    {'district_name': '屏東縣屏東市'},
                    {'district_name': '台南市新市區'},
                    {'district_name': '高雄市路竹區'}
                ]
            }
        }), content_type='application/json')
        self.assertEqual(res.status_code, 201)

    def test_get_quick_search(self):
        res = self.client.post('/quick_search', headers={'Authorization': f'Bearer {self.admin_token}'}, data=json.dumps({
            'name': '南部科學園區',
            'query': {
                'locations': [
                    {'district_name': '屏東縣屏東市'},
                    {'district_name': '台南市新市區'},
                    {'district_name': '高雄市路竹區'}
                ]
            }
        }), content_type='application/json')
        self.assertEqual(res.status_code, 201)

        res = self.client.get('/quick_search/南部科學園區', headers={'Authorization': f'Bearer {self.admin_token}'})
        self.assertEqual(res.status_code, 200)

    def test_run_quick_search(self):
        res = self.client.post('/quick_search', headers={'Authorization': f'Bearer {self.admin_token}'}, data=json.dumps({
            'name': '南部科學園區',
            'query': {
                'locations': [
                    {'district_name': '屏東縣屏東市'},
                    {'district_name': '台南市新市區'},
                    {'district_name': '高雄市路竹區'}
                ]
            }
        }), content_type='application/json')
        self.assertEqual(res.status_code, 201)

        res = self.client.get('/quick_search/run/南部科學園區', headers={'Authorization': f'Bearer {self.user_token}'})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.get_json()), 3)

if __name__ == '__main__':
    unittest.main()
