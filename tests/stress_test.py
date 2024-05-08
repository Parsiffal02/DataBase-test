import psycopg2
import time

# Функция для создания соединения с базой данных
def create_connection():
    try:
        connection = psycopg2.connect(
            user="postgres",
            password="1122",
            host="localhost",
            port="5432",
            database="resto"
        )
        return connection
    except psycopg2.Error as e:
        print("Ошибка при подключении к базе данных:", e)
        return None

# Функция для выполнения запроса и измерения времени выполнения
def execute_query_and_measure_time(connection, query):
    start_time = time.time()
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        execution_time = time.time() - start_time
        print("Время выполнения запроса:", execution_time)
    except psycopg2.Error as e:
        print("Ошибка при выполнении запроса:", e)

# Функция для выполнения нагрузочных тестов
def run_stress_tests():
    connection = create_connection()
    if connection:
        # Тест на чтение большого объема данных
        execute_query_and_measure_time(connection, "SELECT * FROM \"Business\" LIMIT 10000;")
        
        # Тест на обновление данных
        execute_query_and_measure_time(connection, "UPDATE \"Business\" SET address = 'Updated Address' WHERE id = 13;")
        
        # Тест на выполнение сложного запроса
        execute_query_and_measure_time(connection, "SELECT owner, COUNT(*) FROM \"Business\" GROUP BY owner;")
        
        # Тест на удаление данных
        execute_query_and_measure_time(connection, "DELETE FROM \"Business\" WHERE id = 34;")

        connection.close()

# Запуск нагрузочных тестов
run_stress_tests()
