import psycopg2 as ps


class DataBase:
    def __init__(self, user, password, name, host='localhost'):
        self.user = user
        self.password = password
        self.name = name
        self.host = host

        con = ps.connect(
            user=user,
            password=password,
            database='postgres',
            host=host
        )

        con.autocommit = True
        cur = con.cursor()
        cur.execute("SELECT datname FROM pg_database;")

        if (name,) not in cur.fetchall():
            cur.execute(f"CREATE DATABASE {name};")
        con.close()
        cur.close()

        self.connection = ps.connect(
            user=user,
            password=password,
            database=name,
            host=host
        )
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()
        self.cursor.execute(open('initdb.sql', 'r').read())
        self.init_tables()
        self.cursor.execute(open('functions.sql', 'r').read())

    def drop_database(self):
        self.connection = ps.connect(
            user=self.user,
            password=self.password,
            database=self.name,
            host=self.host
        )
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()
        print(f"Dropping database: {self.name}")
        self.cursor.execute(f"DROP DATABASE IF EXISTS {self.name};")
        print("Database dropped successfully")
        self.connection.close()
        self.cursor.close()

    def init_tables(self):
        self.cursor.callproc("init_tables")

    # Owners ---------------------------------------------------------
    def add_owner(self, owner_name, f_date, email):
        self.cursor.callproc("add_owner", (owner_name, f_date, email,))

    def get_owners(self):
        self.cursor.callproc("get_owners")
        return self.cursor.fetchone()[0]

    def delete_owner(self, name):
        self.cursor.callproc("delete_owner", (name,))

    def delete_owners(self):
        self.cursor.callproc("delete_owners")

    def search_owner(self, email):
        self.cursor.callproc("search_owner", (email,))
        return self.cursor.fetchone()[0]

    def update_owner(self, new_name, previous_name):
        self.cursor.callproc("update_owner", (new_name, previous_name,))

    # -------------------------------------------------------------

    # Suppliers ---------------------------------------------------------
    def add_supplier(self, organisation, reviews, phone_number):
        self.cursor.callproc("add_supplier", (organisation, reviews, phone_number,))

    def get_suppliers(self):
        self.cursor.callproc("get_suppliers")
        return self.cursor.fetchone()[0]

    def delete_supplier(self, name):
        self.cursor.callproc("delete_supplier", (name,))

    def delete_suppliers(self):
        self.cursor.callproc("delete_suppliers")

    def search_supplier(self, phone_number):
        self.cursor.callproc("search_supplier", (phone_number,))
        return self.cursor.fetchone()[0]

    def update_supplier(self, new_name, previous_name):
        self.cursor.callproc("update_supplier", (new_name, previous_name,))

    # -------------------------------------------------------------

    # Ratings ---------------------------------------------------------
    def add_rating(self, business_name, feedback, grade):
        self.cursor.callproc("add_rating", (business_name, feedback, grade,))

    def get_ratings(self):
        self.cursor.callproc("get_ratings")
        return self.cursor.fetchone()[0]

    def delete_ratings(self):
        self.cursor.callproc("delete_ratings")

    def search_ratings(self, name):
        self.cursor.callproc("search_ratings", (name,))
        return self.cursor.fetchone()[0]

    def delete_rating(self, name):
        self.cursor.callproc("delete_rating", (name,))

    def update_ratings(self, new_name, previous_name):
        self.cursor.callproc("update_ratings", (new_name, previous_name,))
    # -------------------------------------------------------------

    # Lounge bars ---------------------------------------------------------
    def add_business(self, name, address, supplier, owner, feature):
        self.cursor.callproc("add_business", (name, address, supplier, owner, feature,))

    def search_business(self, name):
        self.cursor.callproc("search_business", (name,))
        return self.cursor.fetchone()[0]

    def get_business(self):
        self.cursor.callproc("get_business")
        return self.cursor.fetchone()[0]

    def delete_business(self, name):
        self.cursor.callproc("delete_business", (name,))

    def delete_businesses(self):
        self.cursor.callproc("delete_businesses")

    def update_business(self, new_name, previous_name):
        self.cursor.callproc("update_business", (new_name, previous_name,))
