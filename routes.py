from resources.user import UserRegister
from resources.item import Item, Items
from resources.store import Store, Stores

def initialize_routes(api):

    # Resource-1 adding to end_point
    api.add_resource(Items, '/items'); # https://127.0.0.1:5000/items  (connection with end_point)

    # Resource-2 adding to end_point
    api.add_resource(Item, '/item/<string:name>') # https://127.0.0.1:5000/items/<name>

    # Resource-3 adding to end_point
    api.add_resource(UserRegister, '/register')

    # Resource-4 adding to end_point
    api.add_resource(Stores, '/stores')

    # Resource-5 adding to end_point
    api.add_resource(Store, '/store')