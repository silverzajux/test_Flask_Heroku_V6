from models.db_operations import connect_to_db
from models.store import StoreModel

class ItemModel():

    def __init__(self,name,price, store):
        self.name = name
        self.price = price
        self.store = store
    
    def json(self):
        return {'name':self.name,'price':self.price,'store':self.store}
    
    @classmethod
    def get_items(cls):
        connection = connect_to_db()
        cursor = connection.cursor()
        sql_query = """SELECT il.name, il.price, s.name store
                         FROM item_list il
              LEFT OUTER JOIN stores s
                           ON s.id = il.store_id
                        WHERE 1=1
                     ORDER BY il.name"""
        cursor.execute(sql_query)
        sql_data = cursor.fetchall()

        new_item_list = []
        for t_item in sql_data:
            # new_item_list.append({'name':t_item[1],'price':t_item[2],'store':t_item[3]}) # or below line
            new_item_list.append(cls(*t_item).json()) # check!
        return new_item_list

    @classmethod
    def find_by_name(cls,name):
        connection = connect_to_db()
        cursor = connection.cursor()

        sql_string = """SELECT il.name, il.price, s.name store
                          FROM item_list il
               LEFT OUTER JOIN stores s
                            ON s.id = il.store_id
                         WHERE il.name = %s"""
        cursor.execute(sql_string, (name,))
        sql_data = cursor.fetchone()
        connection.close()

        if sql_data: # means -> if sql_data is not None
            return cls(*sql_data).json()

        # else return None

    def insert(self):
        connection = connect_to_db()
        cursor = connection.cursor()

        store_item = StoreModel.find_by_name(self.store) # can be checked if None or not
        if store_item is None:
            raise Exception('Store Not Found') # fixed message
        
        sql_string = "INSERT INTO item_list (name, price, store_id) VALUES (%s, %s, %s)"
        cursor.execute(sql_string,(self.name,self.price, store_item['id']))

        connection.commit()
        connection.close()

    def update(self): # update price only!
        connection = connect_to_db()
        cursor = connection.cursor()

        sql_string = "UPDATE item_list SET price = %s WHERE name = %s"
        cursor.execute(sql_string,(self.price,self.name))

        connection.commit()
        connection.close()

    def delete(self):
        connection = connect_to_db()
        cursor = connection.cursor()

        sql_string = "DELETE FROM item_list WHERE name = %s"
        cursor.execute(sql_string,(self.name,))

        connection.commit()
        connection.close()