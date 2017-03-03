from app import app
from db import db

db.init_app(app)

# Flask decorator: run the method before the first request to the app
@app.before_first_request
def create_tables():    # Create tables.
    db.create_all()
