import psycopg2

def create_connection():
    conn = psycopg2.connect(
        dbname="resto",
        user="postgres",
        password="1122",
        host="localhost",
        port="5432"
    )
    return conn
