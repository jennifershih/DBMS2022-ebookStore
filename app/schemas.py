from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(load_only=True, required=True)
    role = fields.Str()

class CommunitySchema(Schema):
    community_id = fields.Int(dump_only=True)
    district_name = fields.Str(required=True)
    community_name = fields.Str(required=True)

class PropertySchema(Schema):
    property_id = fields.Str(required=True)
    community_id = fields.Int(required=True)
    addr_full = fields.Str(required=True)
    floor_no = fields.Int()
    floor_total = fields.Int()
    building_age = fields.Int()
    total_area_ping = fields.Float()
    main_use = fields.Str()
    building_type = fields.Str()

class TransactionSchema(Schema):
    transaction_id = fields.Int(dump_only=True)
    property_id = fields.Str(required=True)
    transaction_date = fields.Date(required=True)
    total_price_10k = fields.Int()
    unit_price_10k_per_ping = fields.Float()
    is_hidden = fields.Bool()

class PointOfInterestSchema(Schema):
    poi_id = fields.Str(required=True)
    community_id = fields.Int(required=True)
    poi_name = fields.Str(required=True)
    category = fields.Str(required=True)
    latitude = fields.Float()
    longitude = fields.Float()

class TransportationSchema(Schema):
    transport_id = fields.Str(required=True)
    community_id = fields.Int(required=True)
    type = fields.Str(required=True)
    name = fields.Str(required=True)
    line_name = fields.Str()
    station_code = fields.Str()
    latitude = fields.Float()
    longitude = fields.Float()

class TransactionSearchSchema(Schema):
    quick_search_name = fields.Str()  # New field for quick search
    community_name = fields.Str()
    address = fields.Str()
    start_date = fields.Date()
    end_date = fields.Date()
    building_type = fields.Str()
    min_age = fields.Int()
    max_age = fields.Int()
    min_price = fields.Int()
    max_price = fields.Int()
    min_floor = fields.Int()
    max_floor = fields.Int()
    min_total_floor = fields.Int()
    max_total_floor = fields.Int()
