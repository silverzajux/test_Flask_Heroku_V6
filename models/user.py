import psycopg2
from models.db_operations import connect_to_db

class UserModel():

    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password
    
    @classmethod
    def find_by_username(cls, username):
        connection = connect_to_db()
        cursor = connection.cursor()

        query_string = "SELECT id, username, password FROM users WHERE username=%s"
        cursor.execute(query_string, (username,)) # second parameter should be an iterable, such as tuple!
        sql_data = cursor.fetchone()
        
        if sql_data is not None:
            user = cls(*sql_data) # or cls(sql_data[0], sql_data[1], sql_data[2])
        else:
            user = None
        
        connection.close()
        return user
    
    @classmethod
    def find_by_userid(cls, _id):
        connection = connect_to_db()
        cursor = connection.cursor()

        query_string = "SELECT * FROM users WHERE id = %s"
        cursor.execute(query_string, (_id,))
        sql_data = cursor.fetchone()

        if sql_data is not None:
            user = cls(*sql_data) # or cls(sql_data[0], sql_data[1], sql_data[2])
        else:
            user = None
        
        connection.close()
        return user
    
    def create_user(self):
        connection = connect_to_db()
        cursor = connection.cursor()

        sql_query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        cursor.execute(sql_query,(self.username,self.password))
        
        sql_query = "SELECT id, username, password FROM users WHERE username = %s"
        cursor.execute(sql_query,(self.username,))
        sql_data = cursor.fetchone()
        
        connection.commit()
        connection.close()
        return {'message':'User {} created with id {}'.format(sql_data[1],sql_data[0])}