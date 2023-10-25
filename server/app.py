from config import Flask, session, request, render_template, db, Migrate, CORS
import os

from classes.scraping import ScrapeSite
from classes.pdf_handling import PdfDataExtractor

app = Flask( __name__ )
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///properties.db'
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
    return site.links, 200
    



if __name__ == '__main__':
    app.run(port=5555, debug=True)