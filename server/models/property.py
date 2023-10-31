from config import db, SM

class Property(db.Model, SM):
    __tablename__ = 'properties'

    id = db.Column(db.Integer, primary_key=True)
    market_value = db.Column(db.String)
    depth_in_feet = db.Column(db.String)
    front_in_feet = db.Column(db.String)
    east = db.Column(db.String)
    north = db.Column(db.String)
    acres = db.Column(db.String)
    parcel_number = db.Column(db.String)
    property_address = db.Column(db.String)
    property_type = db.Column(db.String)
    owners_name = db.Column(db.String)
    owners_address_one = db.Column(db.String)
    owners_address_two = db.Column(db.String)


    # address_id = db.Column(db.Integer, db.ForeignKey('addresses.id'))

    # owner = db.relationship('PropertyOwner', backref='owner', cascade='all, delete-orphan')
    
    def __repr__(self) -> str:
        return f"<Property ID: {self.tax_id}, Property Owner: >"
