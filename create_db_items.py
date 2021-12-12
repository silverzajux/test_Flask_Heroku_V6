import psycopg2

connection = psycopg2.connect(database='testDB',user='postgres',password='admin@local',host='127.0.0.1',port='5432')
print('Connected to database...')
cursor = connection.cursor()

ddl_query = """CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, username VARCHAR(100) UNIQUE NOT NULL, 
                password VARCHAR(100))"""
cursor.execute(ddl_query)
print('table USERS created')

ddl_query = "CREATE TABLE IF NOT EXISTS stores (id SERIAL PRIMARY KEY, name VARCHAR(150) UNIQUE)"
cursor.execute(ddl_query)
print('table STORES created')

ddl_query = """CREATE TABLE IF NOT EXISTS item_list (id SERIAL PRIMARY KEY, name VARCHAR(100) UNIQUE NOT NULL, 
                price REAL, store_id INTEGER NOT NULL, FOREIGN KEY (store_id) REFERENCES stores (id))"""
cursor.execute(ddl_query)
print('table ITEM_LIST created')

connection.commit()
connection.close()
print('Connecttion to database closed')
