from config import Flask, session, request, render_template
from config import Migrate
from config import SQLAlchemy
from config import SerializerMixin as SM
from config import IntegrityError
from config import validates
from config import PdfDataExtractor
from config import ScrapeSite
from config import CORS
import os

db = SQLAlchemy()

app = Flask( __name__ )
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///properties'
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Change to true before deployment
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.post('/get_url')
def get_url():
    URL = request.get_json()
    site = ScrapeSite(URL['url'])
    site.links = []
    site.get_request()
    return site.links, 200
    



if __name__ == '__main__':
    app.run(port=5555, debug=True)