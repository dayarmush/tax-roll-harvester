from config import db, SM

class Owner:
    __tablename__ = 'owners'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Integer)
    address_id = db.Column(db.Integer, db.ForeignKey('addresses.id'))

    def __repr__(self):
        return f"<Owner: {self.name}>"