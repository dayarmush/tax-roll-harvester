from config import db, SM

class Owner:
    __tablename__ = 'owners'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Integer)
    address_id = db.Column(db.Integer, db.ForeignKey('addresses.id'))

    property = db.relationship('PropertyOwner', backref='property', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Owner: {self.name}>"