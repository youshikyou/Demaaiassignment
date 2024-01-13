import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        user='root',
        password='Youshikyou1020!',
        host='localhost',
        database='DemaAI'
    )