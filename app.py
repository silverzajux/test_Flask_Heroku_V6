#from re import DEBUG
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from routes import initialize_routes
from datetime import timedelta, datetime

# This version (FlaskRestfulAppV3) will include flask_SQLAlchemy improvements on project
# but not completed yet (update and delete methods not working!)
# if needed should learn the sqlalchemy basics first!

app = Flask(__name__)
app.secret_key = 'A1@!NaticaGreatSecretKeyNatica!@1A' #will be used in JWT
api = Api(app)

# Note-1: We can change the jwt endpoint name with below line, should be written before jwt object initialization
# app.config(['JWT_AUTH_URL_RULE']) = '\login'   -> login or something else, default is '\auth'
# Note-2: config JWT to expire within half an hour
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
# Note-3: config JWT auth key name to be 'email' instead of default 'username' via below line
# app.config['JWT_AUTH_USERNAME_KEY'] = 'email'

jwt = JWT(app, authenticate, identity) # creates a new endpoint ->  /auth   (automatically added to app, name auth is default)

initialize_routes(api) # create end points

# xxdebug -> think about composite operations endpoint!
#xxdebug line for git and github push
#xxdebug line for git and github pull
#xxdebug line for git and github pull v2

if __name__ == '__main__': # to prevent the following line to run if app.py is referenced (imported) in another file
    app.run(port=5000, debug=True) # execute if only app.py is being run directly
