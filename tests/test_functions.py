import psycopg2
import pytest
from db_connection import create_connection

# Fixture to create a new connection for each test
@pytest.fixture(scope="function")
def conn():
    connection = create_connection()
    yield connection
    connection.close()

# Тестирование SQL инъекций для функции add_rating
def test_sql_injection_add_rating(conn):
    injection_business_name = "'; DROP TABLE \"Ratings\"; --"
    injection_feedback = "'; DROP TABLE \"Ratings\"; --"
    injection_grade = 5
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM add_rating(%s, %s, %s)", (injection_business_name, injection_feedback, injection_grade))
    except psycopg2.errors.SyntaxError as e:
        assert False, f"SQL Injection detected in add_rating function: {e}"
    finally:
        conn.rollback()
        cur.close()

# Тестирование SQL инъекций для функции delete_rating
def test_sql_injection_delete_rating(conn):
    injection_business_name = "'; DROP TABLE \"Ratings\"; --"
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM delete_rating(%s)", (injection_business_name,))
    except psycopg2.errors.SyntaxError as e:
        assert False, f"SQL Injection detected in delete_rating function: {e}"
    finally:
        conn.rollback()
        cur.close()

# Тестирование SQL инъекций для функции search_ratings
def test_sql_injection_search_ratings(conn):
    injection_business_name = "'; DROP TABLE \"Ratings\"; --"
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM search_ratings(%s)", (injection_business_name,))
    except psycopg2.errors.SyntaxError as e:
        assert False, f"SQL Injection detected in search_ratings function: {e}"
    finally:
        conn.rollback()
        cur.close()

# Тестирование SQL инъекций для функции add_supplier
def test_sql_injection_add_supplier(conn):
    injection_organisation = "'; DROP TABLE \"Suppliers\"; --"
    injection_reviews = "'; DROP TABLE \"Suppliers\"; --"
    injection_phone_number = "'; DROP TABLE \"Suppliers\"; --"
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM add_supplier(%s, %s, %s)", (injection_organisation, injection_reviews, injection_phone_number))
    except psycopg2.errors.SyntaxError as e:
        assert False, f"SQL Injection detected in add_supplier function: {e}"
    finally:
        conn.rollback()
        cur.close()

# Тестирование SQL инъекций для функции delete_supplier
def test_sql_injection_delete_supplier(conn):
    injection_organisation = "'; DROP TABLE \"Suppliers\"; --"
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM delete_supplier(%s)", (injection_organisation,))
    except psycopg2.errors.SyntaxError as e:
        assert False, f"SQL Injection detected in delete_supplier function: {e}"
    finally:
        conn.rollback()
        cur.close()

# Тестирование SQL инъекций для функции search_supplier
def test_sql_injection_search_supplier(conn):
    injection_phone_number = "'; DROP TABLE \"Suppliers\"; --"
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM search_supplier(%s)", (injection_phone_number,))
    except psycopg2.errors.SyntaxError as e:
        assert False, f"SQL Injection detected in search_supplier function: {e}"
    finally:
        conn.rollback()
        cur.close()

# Тестирование SQL инъекций для функции update_supplier
def test_sql_injection_update_supplier(conn):
    injection_new_organisation = "'; DROP TABLE \"Suppliers\"; --"
    injection_organisation0 = "'; DROP TABLE \"Suppliers\"; --"
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM update_supplier(%s, %s)", (injection_new_organisation, injection_organisation0))
    except psycopg2.errors.SyntaxError as e:
        assert False, f"SQL Injection detected in update_supplier function: {e}"
    finally:
        conn.rollback()
        cur.close()

# Тестирование SQL инъекций для функции add_owner
def test_sql_injection_add_owner(conn):
    injection_name1 = "'; DROP TABLE \"Owners\"; --"
    injection_foundation_date = "2024-04-18"  # Валидная дата
    injection_email = "'; DROP TABLE \"Owners\"; --"
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM add_owner(%s, %s, %s)", (injection_name1, injection_foundation_date, injection_email))
    except psycopg2.errors.SyntaxError as e:
        assert False, f"SQL Injection detected in add_owner function: {e}"
    finally:
        conn.rollback()
        cur.close()

# Тестирование SQL инъекций для функции delete_owner
def test_sql_injection_delete_owner(conn):
    injection_name0 = "'; DROP TABLE \"Owners\"; --"
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM delete_owner(%s)", (injection_name0,))
    except psycopg2.errors.SyntaxError as e:
        assert False, f"SQL Injection detected in delete_owner function: {e}"
    finally:
        conn.rollback()
        cur.close()

# Тестирование SQL инъекций для функции search_owner
def test_sql_injection_search_owner(conn):
    injection_email0 = "'; DROP TABLE \"Owners\"; --"
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM search_owner(%s)", (injection_email0,))
    except psycopg2.errors.SyntaxError as e:
        assert False, f"SQL Injection detected in search_owner function: {e}"
    finally:
        conn.rollback()
        cur.close()

# Тестирование SQL инъекций для функции update_owner
def test_sql_injection_update_owner(conn):
    injection_new_name = "'; DROP TABLE \"Owners\"; --"
    injection_name0 = "'; DROP TABLE \"Owners\"; --"
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM update_owner(%s, %s)", (injection_new_name, injection_name0))
    except psycopg2.errors.SyntaxError as e:
        assert False, f"SQL Injection detected in update_owner function: {e}"
    finally:
        conn.rollback()
        cur.close()

# Тестирование SQL инъекций для функции add_business
def test_sql_injection_add_business(conn):
    injection_name = "'; DROP TABLE \"Business\"; --"
    injection_address = "Test Address"
    injection_supplier = "Test Supplier"
    injection_owner = "Test Owner"
    injection_feature = "Test Feature"
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM add_business(%s, %s, %s, %s, %s)", (injection_name, injection_address, injection_supplier, injection_owner, injection_feature))
    except psycopg2.errors.SyntaxError as e:
        assert False, f"SQL Injection detected in add_business function: {e}"
    finally:
        conn.rollback()
        cur.close()
