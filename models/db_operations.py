import psycopg2
import os

# this version for Heroku database server
def connect_to_db():
    DATABASE_URL = os.environ['DATABASE_URL']
    connection = psycopg2.connect(DATABASE_URL, sslmode='require')
    return connection

''' This version for Local database server
def connect_to_db():
    connection = psycopg2.connect(database='testDB',user='postgres',password='admin@local',host='127.0.0.1',port='5432')
    return connection
'''