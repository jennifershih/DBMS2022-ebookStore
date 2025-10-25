from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, jwt_required, get_current_user
from app.models import User, Community, Property, Transaction, PointOfInterest, Transportation, QuickSearch
from app.schemas import UserSchema, CommunitySchema, PropertySchema, TransactionSchema, PointOfInterestSchema, TransportationSchema, TransactionSearchSchema

user_schema = UserSchema()
community_schema = CommunitySchema()
property_schema = PropertySchema()
transaction_schema = TransactionSchema()
poi_schema = PointOfInterestSchema()
transportation_schema = TransportationSchema()
transaction_search_schema = TransactionSearchSchema()

from app import db

class UserRegistration(Resource):
    def post(self):
        data = request.get_json()
        errors = user_schema.validate(data)
        if errors:
            return errors, 422

        if User.query.filter_by(username=data['username']).first():
            return {'message': 'User already exists'}, 400
        
        user = User(username=data['username'], role=data.get('role', 'user'))
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()
        return {'message': 'User created successfully'}, 201

class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        errors = user_schema.validate(data)
        if errors:
            return errors, 422

        user = User.query.filter_by(username=data['username']).first()
        
        if user and user.check_password(data['password']):
            access_token = create_access_token(identity=str(user.id))
            return {'access_token': access_token}, 200
        return {'message': 'Invalid credentials'}, 401

class CommunityList(Resource):
    @jwt_required()
    def get(self):
        communities = Community.query.all()
        return community_schema.dump(communities, many=True)

    @jwt_required()
    def post(self):
        current_user = get_current_user()
        if current_user.role != 'admin':
            return {'message': 'Admins only'}, 403
        data = request.get_json()
        errors = community_schema.validate(data)
        if errors:
            return errors, 422
        community = Community(**data)
        db.session.add(community)
        db.session.commit()
        return community_schema.dump(community), 201

class CommunityResource(Resource):
    @jwt_required()
    def get(self, community_id):
        community = Community.query.get_or_404(community_id)
        return community_schema.dump(community)

    @jwt_required()
    def put(self, community_id):
        current_user = get_current_user()
        if current_user.role != 'admin':
            return {'message': 'Admins only'}, 403
        data = request.get_json()
        errors = community_schema.validate(data)
        if errors:
            return errors, 422
        community = Community.query.get_or_404(community_id)
        community.district_name = data['district_name']
        community.community_name = data['community_name']
        db.session.commit()
        return community_schema.dump(community)

    @jwt_required()
    def delete(self, community_id):
        current_user = get_current_user()
        if current_user.role != 'admin':
            return {'message': 'Admins only'}, 403
        community = Community.query.get_or_404(community_id)
        db.session.delete(community)
        db.session.commit()
        return {'message': 'Community deleted'}, 204

class PropertyList(Resource):
    @jwt_required()
    def get(self):
        properties = Property.query.all()
        return property_schema.dump(properties, many=True)

    @jwt_required()
    def post(self):
        current_user = get_current_user()
        if current_user.role != 'admin':
            return {'message': 'Admins only'}, 403
        data = request.get_json()
        errors = property_schema.validate(data)
        if errors:
            return errors, 422
        prop = Property(**data)
        db.session.add(prop)
        db.session.commit()
        return property_schema.dump(prop), 201

class PropertyResource(Resource):
    @jwt_required()
    def get(self, property_id):
        prop = Property.query.get_or_404(property_id)
        return property_schema.dump(prop)

    @jwt_required()
    def put(self, property_id):
        current_user = get_current_user()
        if current_user.role != 'admin':
            return {'message': 'Admins only'}, 403
        data = request.get_json()
        errors = property_schema.validate(data)
        if errors:
            return errors, 422
        prop = Property.query.get_or_404(property_id)
        for key, value in data.items():
            setattr(prop, key, value)
        db.session.commit()
        return property_schema.dump(prop)

    @jwt_required()
    def delete(self, property_id):
        current_user = get_current_user()
        if current_user.role != 'admin':
            return {'message': 'Admins only'}, 403
        prop = Property.query.get_or_404(property_id)
        db.session.delete(prop)
        db.session.commit()
        return {'message': 'Property deleted'}, 204

class TransactionList(Resource):
    @jwt_required()
    def post(self):
        current_user = get_current_user()
        if current_user.role != 'admin':
            return {'message': 'Admins only'}, 403
        data = request.get_json()
        errors = transaction_schema.validate(data)
        if errors:
            return errors, 422
        transaction = Transaction(**data)
        db.session.add(transaction)
        db.session.commit()
        return transaction_schema.dump(transaction), 201

class TransactionResource(Resource):
    @jwt_required()
    def get(self, transaction_id):
        t = Transaction.query.get_or_404(transaction_id)
        return transaction_schema.dump(t)

    @jwt_required()
    def put(self, transaction_id):
        current_user = get_current_user()
        if current_user.role != 'admin':
            return {'message': 'Admins only'}, 403
        data = request.get_json()
        errors = transaction_schema.validate(data)
        if errors:
            return errors, 422
        t = Transaction.query.get_or_404(transaction_id)
        for key, value in data.items():
            setattr(t, key, value)
        db.session.commit()
        return transaction_schema.dump(t)

    @jwt_required()
    def delete(self, transaction_id):
        current_user = get_current_user()
        if current_user.role != 'admin':
            return {'message': 'Admins only'}, 403
        t = Transaction.query.get_or_404(transaction_id)
        db.session.delete(t)
        db.session.commit()
        return {'message': 'Transaction deleted'}, 204

class PointOfInterestList(Resource):
    @jwt_required()
    def get(self):
        pois = PointOfInterest.query.all()
        return poi_schema.dump(pois, many=True)

    @jwt_required()
    def post(self):
        current_user = get_current_user()
        if current_user.role != 'admin':
            return {'message': 'Admins only'}, 403
        data = request.get_json()
        errors = poi_schema.validate(data)
        if errors:
            return errors, 422
        poi = PointOfInterest(**data)
        db.session.add(poi)
        db.session.commit()
        return poi_schema.dump(poi), 201

class PointOfInterestResource(Resource):
    @jwt_required()
    def get(self, poi_id):
        p = PointOfInterest.query.get_or_404(poi_id)
        return poi_schema.dump(p)

    @jwt_required()
    def put(self, poi_id):
        current_user = get_current_user()
        if current_user.role != 'admin':
            return {'message': 'Admins only'}, 403
        data = request.get_json()
        errors = poi_schema.validate(data)
        if errors:
            return errors, 422
        p = PointOfInterest.query.get_or_404(poi_id)
        for key, value in data.items():
            setattr(p, key, value)
        db.session.commit()
        return poi_schema.dump(p)

    @jwt_required()
    def delete(self, poi_id):
        current_user = get_current_user()
        if current_user.role != 'admin':
            return {'message': 'Admins only'}, 403
        p = PointOfInterest.query.get_or_404(poi_id)
        db.session.delete(p)
        db.session.commit()
        return {'message': 'Point of Interest deleted'}, 204

class TransportationList(Resource):
    @jwt_required()
    def get(self):
        transportations = Transportation.query.all()
        return transportation_schema.dump(transportations, many=True)

    @jwt_required()
    def post(self):
        current_user = get_current_user()
        if current_user.role != 'admin':
            return {'message': 'Admins only'}, 403
        data = request.get_json()
        errors = transportation_schema.validate(data)
        if errors:
            return errors, 422
        transportation = Transportation(**data)
        db.session.add(transportation)
        db.session.commit()
        return transportation_schema.dump(transportation), 201

class TransportationResource(Resource):
    @jwt_required()
    def get(self, transport_id):
        t = Transportation.query.get_or_404(transport_id)
        return transportation_schema.dump(t)

    @jwt_required()
    def put(self, transport_id):
        current_user = get_current_user()
        if current_user.role != 'admin':
            return {'message': 'Admins only'}, 403
        data = request.get_json()
        errors = transportation_schema.validate(data)
        if errors:
            return errors, 422
        t = Transportation.query.get_or_404(transport_id)
        for key, value in data.items():
            setattr(t, key, value)
        db.session.commit()
        return transportation_schema.dump(t)

    @jwt_required()
    def delete(self, transport_id):
        current_user = get_current_user()
        if current_user.role != 'admin':
            return {'message': 'Admins only'}, 403
        t = Transportation.query.get_or_404(transport_id)
        db.session.delete(t)
        db.session.commit()
        return {'message': 'Transportation deleted'}, 204

class TransactionSearch(Resource):
    @jwt_required()
    def get(self):
        quick_search_name = request.args.get('name')
        query = db.session.query(Transaction).join(Property).join(Community)

        if quick_search_name:
            quick_searches = QuickSearch.query.filter_by(name=quick_search_name).all()
            if quick_searches:
                from sqlalchemy import or_
                location_filters = []
                for qs in quick_searches:
                    search_query = qs.search_query
                    if 'city' in search_query and 'district' in search_query:
                        address_filter = f"%{search_query['city']}{search_query['district']}%"
                        location_filters.append(Property.addr_full.ilike(address_filter))
                if location_filters:
                    query = query.filter(or_(*location_filters))
            else:
                return transaction_schema.dump([], many=True)

        transactions = query.all()
        return transaction_schema.dump(transactions, many=True)

    @jwt_required()
    def post(self):
        data = request.get_json()
        errors = transaction_search_schema.validate(data)
        if errors:
            return errors, 422
        
        query = db.session.query(Transaction).join(Property).join(Community)

        # Apply other filters
        if 'community_name' in data:
            query = query.filter(Community.community_name.ilike(f"%{data['community_name']}%"))
        if 'address' in data:
            query = query.filter(Property.addr_full.ilike(f"%{data['address']}%"))
        if 'start_date' in data:
            query = query.filter(Transaction.transaction_date >= data['start_date'])
        if 'end_date' in data:
            query = query.filter(Transaction.transaction_date <= data['end_date'])
        if 'building_type' in data:
            query = query.filter(Property.building_type == data['building_type'])
        if 'min_age' in data:
            query = query.filter(Property.building_age >= data['min_age'])
        if 'max_age' in data:
            query = query.filter(Property.building_age <= data['max_age'])
        if 'min_price' in data:
            query = query.filter(Transaction.total_price_10k >= data['min_price'])
        if 'max_price' in data:
            query = query.filter(Transaction.total_price_10k <= data['max_price'])
        if 'min_floor' in data:
            query = query.filter(Property.floor_no >= data['min_floor'])
        if 'max_floor' in data:
            query = query.filter(Property.floor_no <= data['max_floor'])
        if 'min_total_floor' in data:
            query = query.filter(Property.floor_total >= data['min_total_floor'])
        if 'max_total_floor' in data:
            query = query.filter(Property.floor_total <= data['max_total_floor'])

        transactions = query.all()
        return transaction_schema.dump(transactions, many=True)