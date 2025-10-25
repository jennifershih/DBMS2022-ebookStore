from app import db, jwt
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    role = db.Column(db.String(80), nullable=False, default='user')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@jwt.user_lookup_loader
def user_lookup_loader(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.get(identity)

class Community(db.Model):
    community_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    district_name = db.Column(db.String(128))
    community_name = db.Column(db.String(128), nullable=False)
    __table_args__ = (db.UniqueConstraint('district_name', 'community_name', name='uq_comm'),)

class Property(db.Model):
    property_id = db.Column(db.String(64), primary_key=True)
    community_id = db.Column(db.Integer, db.ForeignKey('community.community_id'), nullable=False)
    addr_full = db.Column(db.String(255), nullable=False)
    floor_no = db.Column(db.Integer)
    floor_total = db.Column(db.Integer)
    building_age = db.Column(db.Integer)
    total_area_ping = db.Column(db.Float)
    main_use = db.Column(db.String(64))
    building_type = db.Column(db.String(64))

class Transaction(db.Model):
    transaction_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    property_id = db.Column(db.String(64), db.ForeignKey('property.property_id'), nullable=False)
    transaction_date = db.Column(db.Date, nullable=False)
    total_price_10k = db.Column(db.Integer)
    unit_price_10k_per_ping = db.Column(db.Float)
    is_hidden = db.Column(db.Boolean, default=False)

class PointOfInterest(db.Model):
    poi_id = db.Column(db.String(64), primary_key=True)
    community_id = db.Column(db.Integer, db.ForeignKey('community.community_id'), nullable=False)
    poi_name = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(64), nullable=False)
    latitude = db.Column(db.Double)
    longitude = db.Column(db.Double)

class Transportation(db.Model):
    transport_id = db.Column(db.String(64), primary_key=True)
    community_id = db.Column(db.Integer, db.ForeignKey('community.community_id'), nullable=False)
    type = db.Column(db.String(64), nullable=False)
    name = db.Column(db.String(128), nullable=False)
    line_name = db.Column(db.String(128))
    station_code = db.Column(db.String(64))
    latitude = db.Column(db.Double)
    longitude = db.Column(db.Double)

class QuickSearch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    search_query = db.Column(db.JSON, nullable=False)
