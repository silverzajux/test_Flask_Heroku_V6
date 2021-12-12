import psycopg2

def connect_to_db():
    connection = psycopg2.connect(database='testDB',user='postgres',password='admin@local',host='127.0.0.1',port='5432')
    return connection