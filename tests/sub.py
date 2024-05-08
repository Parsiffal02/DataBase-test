import os
import subprocess
from db_connection import create_connection

# Подключение к базе данных PostgreSQL
conn = create_connection()

# Загрузка содержимого initdb.sql для создания базы данных
with open("initdb.sql", "r") as f:
    init_sql = f.read()

# Выполнение SQL-запросов для создания схемы и данных
cur = conn.cursor()
cur.execute(init_sql)
conn.commit()