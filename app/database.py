import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        user='root',
        password='xxx',
        host='localhost',
        database='DemaAI'
    )