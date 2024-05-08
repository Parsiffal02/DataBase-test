import psycopg2
import time
import pytest
from db_connection import create_connection

# Fixture to create a new cursor for each test
@pytest.fixture(scope="module")
def cursor():
    conn = create_connection()
    cur = conn.cursor()
    yield cur
    cur.close()
    conn.close()

# Fixture to create a new connection for each test
@pytest.fixture(scope="module")
def connection():
    conn = create_connection()
    yield conn
    conn.close()

# Test for performance of query execution
def test_performance_query(cursor):
    start_time = time.time()
    cursor.execute("SELECT * FROM \"Business\" WHERE id = 1")
    execution_time = time.time() - start_time
    print("Execution time for query:", execution_time)

# Test for performance of trigger insert
def test_performance_trigger_insert(cursor):
    start_time = time.time()
    cursor.execute("INSERT INTO \"Suppliers\" (organisation, reviews, phone_number) VALUES ('Test Org', 'Test Reviews', '1234567890')")
    cursor.connection.commit()
    execution_time = time.time() - start_time
    print("Execution time for trigger insert:", execution_time)

# Test for performance of trigger update
def test_performance_trigger_update(cursor):
    start_time = time.time()
    cursor.execute("UPDATE \"Suppliers\" SET reviews = 'Updated Reviews' WHERE organisation = 'Test Org'")
    cursor.connection.commit()
    execution_time = time.time() - start_time
    print("Execution time for trigger update:", execution_time)

# Test for performance of trigger delete
def test_performance_trigger_delete(cursor):
    start_time = time.time()
    cursor.execute("DELETE FROM \"Suppliers\" WHERE organisation = 'Test Org'")
    cursor.connection.commit()
    execution_time = time.time() - start_time
    print("Execution time for trigger delete:", execution_time)

# Test for performance of stored procedure
def test_performance_stored_procedure(cursor):
    start_time = time.time()
    cursor.callproc("update_supplier", ("New Org", "Test Org"))
    cursor.connection.commit()
    execution_time = time.time() - start_time
    print("Execution time for stored procedure:", execution_time)

