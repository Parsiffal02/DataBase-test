import pytest
import psycopg2
from db_connection import create_connection

# Подключение к базе данных PostgreSQL
conn = create_connection()

@pytest.fixture(scope="module")
def setup_database():
    # Инициализация базы данных перед тестированием
    cur = conn.cursor()
    cur.execute(open("initdb.sql", "r").read())
    conn.commit()
    yield
    # Очистка базы данных после завершения тестов
    cur.execute("DROP TABLE \"Business\", \"Suppliers\", \"Owners\", \"Ratings\";")
    conn.commit()

def test_trigger_supplier(setup_database):
    # Тестирование триггера trigger_supplier
    # Вставляем тестовые данные
    cur = conn.cursor()
    cur.execute("INSERT INTO \"Business\" (name, address, supplier, owner, feature) VALUES (%s, %s, %s, %s, %s)",
                ('Business 1', 'Address 1', 'Supplier 1', 'Owner 1', 'Feature 1'))
    cur.execute("INSERT INTO \"Suppliers\" (organisation, reviews, phone_number) VALUES (%s, %s, %s)",
                ('Supplier 1', 'Good supplier', '12345678901'))
    conn.commit()

    # Обновляем поставщика
    cur.execute("UPDATE \"Suppliers\" SET organisation = %s WHERE organisation = %s",
                ('New Supplier', 'Supplier 1'))
    conn.commit()

    # Проверяем, что значение также обновлено в таблице "Business"
    cur.execute("SELECT * FROM \"Business\"")
    result = cur.fetchall()
    for row in result:
        assert row[3] == 'New Supplier'

def test_trigger_owner(setup_database):
    # Тестирование триггера trigger_owner
    # Вставляем тестовые данные
    cur = conn.cursor()
    cur.execute("INSERT INTO \"Business\" (name, address, supplier, owner, feature) VALUES (%s, %s, %s, %s, %s)",
                ('Business 2', 'Address 2', 'Supplier 2', 'Owner 2', 'Feature 2'))
    cur.execute("INSERT INTO \"Owners\" (name, foundation_date, email) VALUES (%s, %s, %s)",
                ('Owner 2', '2023-01-01', 'owner2@example.com'))
    conn.commit()

    # Обновляем владельца
    cur.execute("UPDATE \"Owners\" SET name = %s WHERE name = %s",
                ('New Owner', 'Owner 2'))
    conn.commit()

    # Проверяем, что значение также обновлено в таблице "Business"
    cur.execute("SELECT * FROM \"Business\"")
    result = cur.fetchall()
    for row in result:
        assert row[4] == 'New Owner'

def test_trigger_business(setup_database):
    # Тестирование триггера trigger_business
    # Вставляем тестовые данные
    cur = conn.cursor()
    cur.execute("INSERT INTO \"Business\" (name, address, supplier, owner, feature) VALUES (%s, %s, %s, %s, %s)",
                ('Business 3', 'Address 3', 'Supplier 3', 'Owner 3', 'Feature 3'))
    cur.execute("INSERT INTO \"Ratings\" (business_name, feedback, grade) VALUES (%s, %s, %s)",
                ('Business 3', 'Good business', 5))
    conn.commit()

    # Обновляем имя бизнеса
    cur.execute("UPDATE \"Business\" SET name = %s WHERE name = %s",
                ('New Business', 'Business 3'))
    conn.commit()

    # Проверяем, что значение также обновлено в таблице "Ratings"
    cur.execute("SELECT * FROM \"Ratings\"")
    result = cur.fetchall()
    for row in result:
        assert row[0] == 'New Business'

def teardown_module():
    # Закрытие соединения с базой данных после всех тестов
    conn.close()
