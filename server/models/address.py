from config import db, SM

class Address:
    __tablename__ = 'addresses'

    id = db.Column(db.Integer, primary_key=True)
    street_address = db.Column(db.String)
    street_address_2 = db.Column(db.String)
    state = db.Column(db.String)
    city = db.Column(db.String)
    zipcode = db.Column(db.String)
    address_type = db.Column(db.String)

    property = db.relationship('Property', backref='address', cascade='all, delete-orphan')
    owner = db.relationship('Owner', backref='address', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Property Address: {self.street_address}>"