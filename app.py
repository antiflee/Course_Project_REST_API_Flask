import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','sqlite:///data.db') # Tells the system that the sqlite database is at the root folder at the project. This sqlite can also be MySQL etc.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Tells the Flask sqlalchemy tracker not to track, because SQLAlchemy itself has its own tracker. This line is just to save some cpu.
app.secret_key = 'jose'
api = Api(app)



# JWT is used to facilitate authentication method.
jwt = JWT(app, authenticate, identity) # /auth will be created by JWT autimatically.

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/item')
api.add_resource(StoreList, '/store')
api.add_resource(UserRegister, '/register')

if __name__== '__main__':
    from db import db
    db.init_app(app)
    app.run(port=8000, debug=True)
