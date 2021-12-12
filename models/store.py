import psycopg2
from models.db_operations import connect_to_db

class StoreModel():

    def __init__(self,_id,name):
        self.id = _id
        self.name = name
    
    def json(self):
        return {'id':self.id,'name':self.name}
    
    @classmethod
    def get_stores(cls):
        print('XXDEBUG - 6.1')
        store_list = []
        
        connection = connect_to_db()
        cursor = connection.cursor()
        print('XXDEBUG - 6.2')
        sql_query = """SELECT s.id, s.name
                         FROM stores s
                        WHERE 1=1"""
        cursor.execute(sql_query)
        sql_data = cursor.fetchall()
        print('XXDEBUG - 6.3')
        
        for store in sql_data:
            store_list.append({'id':store[0],'name':store[1]})
        
        return store_list

    @classmethod
    def find_by_name(cls,name):
        connection = connect_to_db()
        cursor = connection.cursor()

        sql_query = """SELECT s.id, s.name
                         FROM stores s
                        WHERE s.name = %s"""
        cursor.execute(sql_query,(name,))
        sql_data = cursor.fetchone()

        if sql_data:
            return cls(*sql_data).json()
    
    def insert(self):
        connection = connect_to_db()
        cursor = connection.cursor()

        sql_query = "INSERT INTO stores (name) VALUES (%s)"
        cursor.execute(sql_query,(self.name,))

        connection.commit()
        connection.close()
    
    def update(self):
        connection = connect_to_db()
        cursor = connection.cursor()

        sql_query = "UPDATE stores SET name=%s WHERE id=%s"
        cursor.execute(sql_query,(self.name, self.id))

        connection.commit()
        connection.close()
    
    def delete(self):
        connection = connect_to_db()
        cursor = connection.cursor()

        sql_query = "DELETE FROM stores WHERE name=%s"
        cursor.execute(sql_query,(self.name,))

        connection.commit()
        connection.close()

