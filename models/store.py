from db import db

class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def json(self):                                     # Without this method, in the resources package, using return item will return an object, instead of a json dictionary.
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]} # Don't forget the .all(), because we used the lazy='dynamic' to save some time.

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
