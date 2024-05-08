import psycopg2
import timeit
from db_connection import create_connection

# Подключение к базе данных PostgreSQL
conn = create_connection()

def test_performance():
    # Проверка производительности запроса
    cur = conn.cursor()
    start_time = timeit.default_timer()
    cur.execute("SELECT * FROM \"Business\"")
    end_time = timeit.default_timer()
    elapsed_time = end_time - start_time
    print("Time taken to execute query:", elapsed_time)

    # Проверка, что запрос выполнился за приемлемое время
    assert elapsed_time < 0.1, "Query took too long to execute"

    conn.commit()

def teardown_module():
    # Закрытие соединения с базой данных
    conn.close()
