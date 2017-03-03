from db import db

class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):                                     # Without this method, in the resources package, using return item will return an object, instead of a json dictionary.
        return {'name': self.name, 'price': self.price} # Now we can use return item.json() to return a json styled dictionary.

    @classmethod
    def find_by_name(cls, name):
        # Returns an ItemModel object
        return cls.query.filter_by(name=name).first()     # Method query is from db.Model. Equivalent to SELECT * FROM items WHERE name=name LIMIT 1

    def save_to_db(self):
        # This method can both insert and update
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
