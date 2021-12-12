from models.user import UserModel
from werkzeug.security import safe_str_cmp

def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user is not None and safe_str_cmp(user.password, password):
        return user

def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_userid(user_id)
