from config import db, SM

class PropertyOwner:
    __tablename__ = 'owners_properties'

    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'))
    owner_id = db.Column(db.Integer, db.ForeignKey('owners.id'))
    

