from app import app
from config import db
from models.property import Property

if __name__ == '__main__':
    with app.app_context():
        print('Deleting')
        Property.query.delete()
        db.session.commit()