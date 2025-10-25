from app import create_app, db
from app.models import User, Community, Property, Transaction, PointOfInterest, Transportation, QuickSearch
from datetime import date

def seed_data():
    app = create_app()
    with app.app_context():
        # Drop all tables and recreate them
        db.drop_all()
        db.create_all()
        
        # Create users
        if not User.query.filter_by(username='admin').first():
            admin_user = User(username='admin', role='admin')
            admin_user.set_password('admin')
            db.session.add(admin_user)

        if not User.query.filter_by(username='user').first():
            user = User(username='user', role='user')
            user.set_password('user')
            db.session.add(user)

        db.session.commit()

        # Create communities
        if not Community.query.filter_by(district_name='竹北市', community_name='縣治里').first():
            community1 = Community(district_name='竹北市', community_name='縣治里')
            db.session.add(community1)
        if not Community.query.filter_by(district_name='南屯區', community_name='文山里').first():
            community2 = Community(district_name='南屯區', community_name='文山里')
            db.session.add(community2)
        db.session.commit()

        community1 = Community.query.filter_by(district_name='竹北市', community_name='縣治里').first()
        community2 = Community.query.filter_by(district_name='南屯區', community_name='文山里').first()

        # Create properties
        if not Property.query.filter_by(property_id='A001').first():
            property1 = Property(property_id='A001', community_id=community1.community_id, addr_full='竹北市縣治一街1號', floor_no=5, floor_total=10, building_age=10, total_area_ping=30.5, main_use='住家', building_type='大樓')
            db.session.add(property1)
        if not Property.query.filter_by(property_id='A002').first():
            property2 = Property(property_id='A002', community_id=community1.community_id, addr_full='竹北市縣治一街2號', floor_no=3, floor_total=7, building_age=5, total_area_ping=40.2, main_use='住家', building_type='華廈')
            db.session.add(property2)
        if not Property.query.filter_by(property_id='B001').first():
            property3 = Property(property_id='B001', community_id=community2.community_id, addr_full='南屯區文山一街1號', floor_no=2, floor_total=5, building_age=20, total_area_ping=50.0, main_use='住家', building_type='公寓')
            db.session.add(property3)
        if not Property.query.filter_by(property_id='B002').first():
            property4 = Property(property_id='B002', community_id=community2.community_id, addr_full='南屯區文山一街2號', floor_no=1, floor_total=3, building_age=30, total_area_ping=60.7, main_use='店面', building_type='透天')
            db.session.add(property4)
        db.session.commit()

        property1 = Property.query.filter_by(property_id='A001').first()
        property2 = Property.query.filter_by(property_id='A002').first()
        property3 = Property.query.filter_by(property_id='B001').first()
        property4 = Property.query.filter_by(property_id='B002').first()

        # Create transactions
        if not Transaction.query.filter_by(property_id='A001', transaction_date=date(2023, 1, 1)).first():
            transaction1 = Transaction(property_id=property1.property_id, transaction_date=date(2023, 1, 1), total_price_10k=1000, unit_price_10k_per_ping=32.8)
            db.session.add(transaction1)
        if not Transaction.query.filter_by(property_id='A001', transaction_date=date(2023, 2, 1)).first():
            transaction2 = Transaction(property_id=property1.property_id, transaction_date=date(2023, 2, 1), total_price_10k=1050, unit_price_10k_per_ping=34.4)
            db.session.add(transaction2)
        if not Transaction.query.filter_by(property_id='A002', transaction_date=date(2023, 3, 1)).first():
            transaction3 = Transaction(property_id=property2.property_id, transaction_date=date(2023, 3, 1), total_price_10k=1200, unit_price_10k_per_ping=29.8)
            db.session.add(transaction3)
        if not Transaction.query.filter_by(property_id='A002', transaction_date=date(2023, 4, 1)).first():
            transaction4 = Transaction(property_id=property2.property_id, transaction_date=date(2023, 4, 1), total_price_10k=1250, unit_price_10k_per_ping=31.1)
            db.session.add(transaction4)
        if not Transaction.query.filter_by(property_id='B001', transaction_date=date(2023, 5, 1)).first():
            transaction5 = Transaction(property_id=property3.property_id, transaction_date=date(2023, 5, 1), total_price_10k=2000, unit_price_10k_per_ping=40.0)
            db.session.add(transaction5)
        if not Transaction.query.filter_by(property_id='B001', transaction_date=date(2023, 6, 1)).first():
            transaction6 = Transaction(property_id=property3.property_id, transaction_date=date(2023, 6, 1), total_price_10k=2050, unit_price_10k_per_ping=41.0)
            db.session.add(transaction6)
        if not Transaction.query.filter_by(property_id='B002', transaction_date=date(2023, 7, 1)).first():
            transaction7 = Transaction(property_id=property4.property_id, transaction_date=date(2023, 7, 1), total_price_10k=3000, unit_price_10k_per_ping=49.4)
            db.session.add(transaction7)
        if not Transaction.query.filter_by(property_id='B002', transaction_date=date(2023, 8, 1)).first():
            transaction8 = Transaction(property_id=property4.property_id, transaction_date=date(2023, 8, 1), total_price_10k=3050, unit_price_10k_per_ping=50.2)
            db.session.add(transaction8)
        db.session.commit()

        # Create points of interest
        if not PointOfInterest.query.filter_by(poi_id='P001').first():
            poi1 = PointOfInterest(poi_id='P001', community_id=community1.community_id, poi_name='竹北國小', category='學校', latitude=24.83, longitude=121.01)
            db.session.add(poi1)
        if not PointOfInterest.query.filter_by(poi_id='P002').first():
            poi2 = PointOfInterest(poi_id='P002', community_id=community1.community_id, poi_name='竹北公園', category='公園', latitude=24.83, longitude=121.02)
            db.session.add(poi2)
        if not PointOfInterest.query.filter_by(poi_id='P003').first():
            poi3 = PointOfInterest(poi_id='P003', community_id=community2.community_id, poi_name='文山國小', category='學校', latitude=24.15, longitude=120.62)
            db.session.add(poi3)
        if not PointOfInterest.query.filter_by(poi_id='P004').first():
            poi4 = PointOfInterest(poi_id='P004', community_id=community2.community_id, poi_name='文山公園', category='公園', latitude=24.15, longitude=120.63)
            db.session.add(poi4)
        db.session.commit()

        # Create transportations
        if not Transportation.query.filter_by(transport_id='T001').first():
            transportation1 = Transportation(transport_id='T001', community_id=community1.community_id, type='捷運', name='竹北站', line_name='紅線', station_code='R10', latitude=24.83, longitude=121.01)
            db.session.add(transportation1)
        if not Transportation.query.filter_by(transport_id='T002').first():
            transportation2 = Transportation(transport_id='T002', community_id=community1.community_id, type='公車', name='300路', line_name='竹北市區公車', latitude=24.83, longitude=121.02)
            db.session.add(transportation2)
        if not Transportation.query.filter_by(transport_id='T003').first():
            transportation3 = Transportation(transport_id='T003', community_id=community2.community_id, type='捷運', name='文心森林公園站', line_name='綠線', station_code='G10a', latitude=24.15, longitude=120.64)
            db.session.add(transportation3)
        if not Transportation.query.filter_by(transport_id='T004').first():
            transportation4 = Transportation(transport_id='T004', community_id=community2.community_id, type='公車', name='100路', line_name='台中市區公車', latitude=24.15, longitude=120.63)
            db.session.add(transportation4)
        db.session.commit()

        # Create quick search data
        quick_search_data = [
            {'name': '新竹科學園區', 'search_query': {'city': '新竹市', 'district': '東區'}},
            {'name': '新竹科學園區', 'search_query': {'city': '新竹縣', 'district': '寶山鄉'}},
            {'name': '新竹生物醫學園區', 'search_query': {'city': '新竹縣', 'district': '竹北市'}},
            {'name': '竹南園區', 'search_query': {'city': '苗栗縣', 'district': '竹南鎮'}},
            {'name': '竹南園區', 'search_query': {'city': '苗栗縣', 'district': '頭份市'}},
            {'name': '銅鑼園區', 'search_query': {'city': '苗栗縣', 'district': '銅鑼鄉'}},
            {'name': '龍潭園區', 'search_query': {'city': '桃園市', 'district': '龍潭區'}},
            {'name': '宜蘭園區', 'search_query': {'city': '宜蘭縣', 'district': '宜蘭市'}},
            {'name': '宜蘭園區', 'search_query': {'city': '宜蘭縣', 'district': '員山鄉'}},
            {'name': '中部科學園區', 'search_query': {'city': '臺中市', 'district': '西屯區'}},
            {'name': '中部科學園區', 'search_query': {'city': '臺中市', 'district': '大雅區'}},
            {'name': '后里園區', 'search_query': {'city': '臺中市', 'district': '后里區'}},
            {'name': '虎尾園區', 'search_query': {'city': '雲林縣', 'district': '虎尾鎮'}},
            {'name': '二林園區', 'search_query': {'city': '彰化縣', 'district': '二林鎮'}},
            {'name': '中興園區', 'search_query': {'city': '南投縣', 'district': '南投市'}},
            {'name': '臺南園區', 'search_query': {'city': '臺南市', 'district': '新市區'}},
            {'name': '臺南園區', 'search_query': {'city': '臺南市', 'district': '善化區'}},
            {'name': '臺南園區', 'search_query': {'city': '臺南市', 'district': '安定區'}},
            {'name': '高雄園區', 'search_query': {'city': '高雄市', 'district': '路竹區'}},
            {'name': '高雄第二園區', 'search_query': {'city': '高雄市', 'district': '橋頭區'}},
            {'name': '高雄第三園區', 'search_query': {'city': '高雄市', 'district': '楠梓區'}},
            {'name': '嘉義園區', 'search_query': {'city': '嘉義縣', 'district': '太保市'}},
            {'name': '屏東園區', 'search_query': {'city': '屏東縣', 'district': '屏東市'}},
            {'name': '屏東園區', 'search_query': {'city': '屏東縣', 'district': '長治鄉'}},
        ]

        # Clear existing quick search data
        QuickSearch.query.delete()
        
        # Add all quick search data
        for data in quick_search_data:
            quick_search = QuickSearch(
                name=data['name'],
                search_query=data['search_query'],
                city=data['search_query']['city'],
                district=data['search_query']['district']
            )
            db.session.add(quick_search)
        
        db.session.commit()

        print("Test data created successfully!")

if __name__ == '__main__':
    seed_data()