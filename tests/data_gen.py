import psycopg2
from psycopg2 import IntegrityError
from faker import Faker
import random
from db_connection import create_connection

# Подключение к базе данных PostgreSQL
conn = create_connection()

# Создание объекта Faker
faker = Faker()

# Функция для генерации случайных данных и вставки их в таблицу "Business"
def insert_business_data(conn):
    cur = conn.cursor()
    for _ in range(100000):  # Генерация 100000 записей
        name = faker.company()
        address = faker.address()
        supplier = faker.company()
        owner = faker.name()
        feature = faker.word()
        try:
            cur.execute("INSERT INTO \"Business\" (name, address, supplier, owner, feature) VALUES (%s, %s, %s, %s, %s)", (name, address, supplier, owner, feature))
        except IntegrityError:
            pass  # Пропускаем дубликаты
    conn.commit()
    print("Business data added successfully!")

# Функция для генерации случайных данных и вставки их в таблицу "Suppliers"
def insert_suppliers_data(conn):
    cur = conn.cursor()
    for _ in range(20000):  # Генерация 20000 записей
        organisation = faker.company()
        reviews = faker.text()
        phone_number = faker.numerify(text='###########')  # Генерация номера телефона без дополнительных символов
        try:
            cur.execute("INSERT INTO \"Suppliers\" (organisation, reviews, phone_number) VALUES (%s, %s, %s)", (organisation, reviews, phone_number))
        except IntegrityError:
            pass  # Пропускаем дубликаты
    conn.commit()
    print("Suppliers data added successfully!")

# Функция для генерации случайных данных и вставки их в таблицу "Owners"
def insert_owners_data(conn):
    cur = conn.cursor()
    for _ in range(50000):  # Генерация 50000 записей
        name = faker.name()
        foundation_date = faker.date_of_birth(minimum_age=18, maximum_age=90).strftime('%Y-%m-%d')
        email = faker.email()
        try:
            cur.execute("INSERT INTO \"Owners\" (name, foundation_date, email) VALUES (%s, %s, %s)", (name, foundation_date, email))
        except IntegrityError:
            pass  # Пропускаем дубликаты
    conn.commit()
    print("Owners data added successfully!")

# Функция для генерации случайных данных и вставки их в таблицу "Ratings"
def insert_ratings_data(conn):
    cur = conn.cursor()
    for _ in range(50000):  # Генерация 50000 записей
        business_name = faker.company()
        feedback = faker.text()
        grade = random.randint(1, 5)
        try:
            cur.execute("INSERT INTO \"Ratings\" (business_name, feedback, grade) VALUES (%s, %s, %s)", (business_name, feedback, grade))
        except IntegrityError:
            pass  # Пропускаем дубликаты
    conn.commit()
    print("Ratings data added successfully!")

# Вызов функций для вставки данных
insert_business_data(conn)
insert_suppliers_data(conn)
insert_owners_data(conn)
insert_ratings_data(conn)

# Закрытие соединения с базой данных
conn.close()
