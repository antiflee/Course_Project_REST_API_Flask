from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,  # price value is required for this put method
        help="This field cannot be left blank!"
    )
    parser.add_argument('store_id',
        type=int,
        required=True,  # price value is required for this put method
        help="Every item needs a store id."
    )

    @jwt_required() # Now we have to be authenticated before we can use the GET method.
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message':'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:         # Similar to function(err, var){if(err){...}}
            return {"message": "An error occurred inserting the item."}, 500 # 500: internal server error

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {"message": "Item deleted"}

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if not item:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
            item.store_id = data['store_id']

        item.save_to_db()   # SQLAlchemy will handle whether item._id exists in the db or not to decide using UPDATE or INSERT

        return item.json(), 201


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}   # Or alternatively: list(map(lambda x: x.json(), ItemModel.query.all()))
