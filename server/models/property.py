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
    property_id = db.Column(db.String)
    property_address = db.Column(db.String)
    property_type = db.Column(db.String)
    owners_name = db.Column(db.String)
    owners_address_one = db.Column(db.String)
    owners_address_two = db.Column(db.String)

    def __repr__(self) -> str:
        return f"<Property ID: {self.property_id}, Property Owner: {self.ow}>"
