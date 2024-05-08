import psycopg2
import pytest
from db_connection import create_connection

# Подключение к базе данных PostgreSQL
conn = create_connection()


def test_objects_exist():
    # Проверка наличия всех необходимых объектов в базе данных
    cur = conn.cursor()
    cur.execute("SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name = 'Business')")
    assert cur.fetchone()[0] == True, "Table 'Business' does not exist"
    
    cur.execute("SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name = 'Suppliers')")
    assert cur.fetchone()[0] == True, "Table 'Suppliers' does not exist"
    
    cur.execute("SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name = 'Owners')")
    assert cur.fetchone()[0] == True, "Table 'Owners' does not exist"
    
    cur.execute("SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name = 'Ratings')")
    assert cur.fetchone()[0] == True, "Table 'Ratings' does not exist"
    
    conn.commit()

def test_objects_properties():
    # Проверка свойств объектов
    cur = conn.cursor()
    cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'Business'")
    columns = [row[0] for row in cur.fetchall()]
    assert set(columns) == {'id', 'name', 'address', 'supplier', 'owner', 'feature'}, "Incorrect columns in table 'Business'"

    cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'Suppliers'")
    columns = [row[0] for row in cur.fetchall()]
    assert set(columns) == {'organisation', 'reviews', 'phone_number'}, "Incorrect columns in table 'Suppliers'"

    cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'Owners'")
    columns = [row[0] for row in cur.fetchall()]
    assert set(columns) == {'name', 'foundation_date', 'email'}, "Incorrect columns in table 'Owners'"

    cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'Ratings'")
    columns = [row[0] for row in cur.fetchall()]
    assert set(columns) == {'business_name', 'feedback', 'grade'}, "Incorrect columns in table 'Ratings'"

    conn.commit()

def teardown_module():
    # Закрытие соединения с базой данных
    conn.close()
