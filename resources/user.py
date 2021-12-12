from re import A
from flask_restful import Resource, reqparse
from models.user import UserModel

# Resource-3 definition
class UserRegister(Resource):

    # parser definiton
    parser = reqparse.RequestParser() # initialize a new request parser
    #if parser used, all fields must be added as arguments, otherwise cannot get into request data
    parser.add_argument('username',
        type=str,
        required=True,
        help='cannot be blank and data type must be str'
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help='cannot be blank and data type must be str'
    )

    def post(self):
        request_data = UserRegister.parser.parse_args() # get request data with parser rules

        # check username exists, if no create user else return warning message
        try:
            s_user = UserModel.find_by_username(request_data['username'])
        except Exception as e:
            print(e)
            return {'message':'An error occured while searching {}'.format(request_data['username'])}, 500  # Internal Server Error
        if s_user is not None:
            return {'message':'User {} is already exists in our system'.format(s_user.username)}
        
        # create user
        try:
            # new_user = UserModel.create_user(request_data['username'],request_data['password'])
            new_user = UserModel(None,request_data['username'],request_data['password'])
            result = new_user.create_user()
        except Exception as e:
            print(e)
            return {'message':'An error occured while registering {}'.format(request_data['username'])}, 500  # Internal Server Error
        
        return result
