from app.resources import UserRegistration, UserLogin, CommunityList, CommunityResource, PropertyList, PropertyResource, TransactionList, TransactionResource, PointOfInterestList, PointOfInterestResource, TransportationList, TransportationResource, TransactionSearch

def initialize_routes(api):
    api.add_resource(UserRegistration, '/register')
    api.add_resource(UserLogin, '/login')
    api.add_resource(CommunityList, '/communities')
    api.add_resource(CommunityResource, '/communities/<int:community_id>')
    api.add_resource(PropertyList, '/properties')
    api.add_resource(PropertyResource, '/properties/<string:property_id>')
    api.add_resource(TransactionList, '/transactions')
    api.add_resource(TransactionResource, '/transactions/<int:transaction_id>')
    api.add_resource(PointOfInterestList, '/pois')
    api.add_resource(PointOfInterestResource, '/pois/<string:poi_id>')
    api.add_resource(TransportationList, '/transportations')
    api.add_resource(TransportationResource, '/transportations/<string:transport_id>')
    api.add_resource(TransactionSearch, '/transactions/search')
