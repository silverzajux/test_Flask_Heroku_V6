from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from models.store import StoreModel

class Stores(Resource):

    @jwt_required()
    def get(self):
        try:
            store_list = StoreModel.get_stores()
        except Exception as e:
            print(e)
            return {'message':'Store list cannot being retrieved'}, 500
        
        return {'stores':store_list}

class Store(Resource):
    # CRUD -> POST, GET, PUT, DELETE
    parser = reqparse.RequestParser()
    parser.add_argument('name',
        type=str,
        required=True,
        help='cannot be blank and data type must be string'
    )

    @jwt_required()
    def post(self):
        try:
            request_data = Store.parser.parse_args() # get request data with parser rules
            store_object = StoreModel(0,request_data['name'])
            store = StoreModel.find_by_name(store_object.name)
        except Exception as e:
            print(e)
            return {'message':'An error occured while searching the store {}'.format(store_object.name)}, 500  # Internal Server Error
        
        if store is not None:
            return {'message':'Store {} already exists'.format(store['name'])}, 400 # bad request

        try:
            store_object.insert()
            return {'message':'Store {} created'.format(store_object.name)}
        except Exception as e:
            print(e)
            return {'message':'An error occured while inserting the store {}'.format(store_object.name)}, 500

    # continue here with implementing get, put and delete end points

    # get
    @jwt_required()
    def get(self):
        request_data = Store.parser.parse_args()
        try:
            store_data = StoreModel.find_by_name(request_data['name'])
        except Exception as e:
            print(e)
            return {'message':'An error occured while searching the store {}'.format(request_data['name'])}, 500
        if store_data is None:
            return {'message':'Store {} does not exists'.format(request_data['name'])}, 400
        return store_data

    # delete
    def delete(self):
        request_data = Store.parser.parse_args()
        try:
            store_data = StoreModel.find_by_name(request_data['name'])
        except Exception as e:
            print(e)
            return {'message':'An error occured while searching the store {}'.format(request_data['name'])}, 500
        if store_data is None:
            return {'message':'Store {} does not exists'.format(request_data['name'])}, 400
        try:
            store_object = StoreModel(store_data['id'],store_data['name'])
            store_object.delete() # Note: if store exists in items table then will get foreign key constraint error
            return {'message':'Store {} deleted'.format(store_object.name)}
        except Exception as e:
            print(e)
            return {'message':'An error occured while deleting the store {}'.format(store_object.name)}, 500