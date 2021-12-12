from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from models.item import ItemModel

# Resource-1 definiton 
class Items(Resource):
    @jwt_required()
    def get(self): # to return all items
        try:
            item_list = ItemModel.get_items()
        except Exception as e:
            print(e)
            return {'message':'Items cannot being retrieved'}, 500 # Internal Server Error

        return {'items':item_list}


# Resource-2 definitions
class Item(Resource):

    parser = reqparse.RequestParser() # initialize a new request parser
    #if parser used, all fields must be added as arguments, otherwise cannot get into request data
    parser.add_argument('price',
        type=float,
        required=True,
        help='cannot be blank and data type must be float'
    )
    parser.add_argument('store',
        type=str,
        required=True,
        help='cannot be blank and data type must be string'
    )
    
    @jwt_required()
    def get(self,name): # to return specific item
        try:
            item = ItemModel.find_by_name(name)
        except Exception as e:
            print(e)
            return {'message':'An error occured while searcing the item'}, 500  # Internal Server Error
        if item is not None:
            return item
        return {'message':'Item {} does not exists'.format(name)}, 404  # Not found

    @jwt_required()
    def post(self,name): # to Create an item
        try:
            item = ItemModel.find_by_name(name)
        except Exception as e:
            print(e)
            return {'message':'An error occured while searching {}'.format(name)}, 500  # Internal Server Error
        
        if item is not None:
            return {'message':'Item {} is already exists'.format(name)}, 400 # bad request
        
        request_data = Item.parser.parse_args() # get request data with parser rules
        requested_item = ItemModel(name, request_data['price'], request_data['store'])

        try:
            requested_item.insert()
            return {'message':'Item {} created'.format(requested_item.name)}
        except Exception as e:
            print(e)
            if str(e) == 'Store Not Found':
                return {'message':'{} is invalid store name'.format(requested_item.store)}
            else:
                print(e)
                return {'message':'An error occured while inserting {}'.format(requested_item.name)}, 500  # Internal Server Error    
    
    @jwt_required()
    def put(self,name): # to update an item
        try:
            db_item = ItemModel.find_by_name(name)
        except Exception as e:
            print(e)
            return {'message':'An error occured while searching {}'.format(name)}, 500  # Internal Server Error
        
        if db_item is None:
            return {'message':'Item you are trying to update does not exists'}, 400 # bad request

        try:
            request_data = Item.parser.parse_args()
            request_item = ItemModel(name,request_data['price'],request_data['store'])

            request_item.update()
            return {'message':'Item {} updated'.format(request_item.name)}
        except Exception as e:
            print(e)
            return {'message':'An error occured while updating {}'.format(request_item.name)}, 500  # Internal Server Error  
    
    @jwt_required()
    def delete(self,name): # to Delete an item
        try:
            item = ItemModel.find_by_name(name)
        except Exception as e:
            print(e)
            return {'message':'An error occured while searching the item'}, 500  # Internal Server Error

        if item is None:
            return {'message':'Item you are trying to delete does not exists'}, 400 # bad request

        del_item = ItemModel(item['name'],item['price'],item['store']) # store and price can be passed None here
        
        try:
            del_item.delete()
            return {'message':'Item {} deleted'.format(del_item.name)}
        except Exception as e:
            print(e)
            return {'message':'An error occured while deleting the item'}, 500  # Internal Server Error