from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QHeaderView, QTableWidgetItem

import dbConnection
import userInterface
from database import DataBase


class ConnectWindow(QtWidgets.QMainWindow, dbConnection.Ui_connectDatabase):
    def __init__(self, app):
        super().__init__()
        self.setupUi(self)

        self.app = app
        self.connectButton.clicked.connect(self.connect_to)

    def connect_to(self):
        self.app.connect_to_database(self.userNameText.text(), self.passwordText.text(), self.databaseNameText.text())
        self.close()


class MainWindow(QtWidgets.QMainWindow, userInterface.Ui_MainWindow):
    def __init__(self, ):
        super().__init__()
        self.setupUi(self)
        self.db = None
        self.changed = False
        self.connectWindow = ConnectWindow(self)
        self.columns_business = ['name', 'address', 'supplier', 'owner', 'feature']
        self.columns_ratings = ['business_name', 'feedback', 'grade']
        self.columns_owners = ['name', 'foundation_date', 'email']
        self.columns_suppliers = ['organisation', 'reviews', 'phone_number']

        # Toolbar
        self.actionConnect.triggered.connect(self.connectWindow.show)
        self.actionClear_Tables.triggered.connect(self.clear_all)
        self.actionDelete_database.triggered.connect(self.drop_database)

        # Owners
        self.ownersTable.setColumnCount(len(self.columns_owners))
        self.ownersTable.setHorizontalHeaderLabels(self.columns_owners)
        self.ownersTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.addOwnersButton.clicked.connect(self.add_owner)
        self.deleteOwnersButton.clicked.connect(self.delete_owner)
        self.searchOwnersButton.clicked.connect(self.search_owner)
        self.clearOwnersButton.clicked.connect(self.delete_owners)
        self.ownersTable.itemChanged.connect(self.update_owner)

        # Suppliers
        self.suppliersTable.setColumnCount(len(self.columns_suppliers))
        self.suppliersTable.setHorizontalHeaderLabels(self.columns_suppliers)
        self.suppliersTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.addSuppliersButton.clicked.connect(self.add_supplier)
        self.deleteSuppliersButton.clicked.connect(self.delete_supplier)
        self.searchSuppliersButton.clicked.connect(self.search_supplier)
        self.clearSuppliersButton.clicked.connect(self.delete_suppliers)
        self.suppliersTable.itemChanged.connect(self.update_supplier)

        # Ratings
        self.ratingsTable.setColumnCount(len(self.columns_ratings))
        self.ratingsTable.setHorizontalHeaderLabels(self.columns_ratings)
        self.ratingsTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.addRatingsButton.clicked.connect(self.add_rating)
        self.searchRatingsButton.clicked.connect(self.search_ratings)
        self.deleteRatingsButton.clicked.connect(self.delete_rating)
        self.clearRatingsButton.clicked.connect(self.delete_ratings)

        # Lounge bars
        self.BusinessTable.setColumnCount(len(self.columns_business))
        self.BusinessTable.setHorizontalHeaderLabels(self.columns_business)
        self.BusinessTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.addButton.clicked.connect(self.add_business)
        self.deleteButton.clicked.connect(self.delete_business)
        self.searchButton.clicked.connect(self.search_business)
        self.clearButton.clicked.connect(self.delete_businesses)
        self.BusinessTable.itemChanged.connect(self.update_business)

    def connect_to_database(self, user, pswd, name, host='localhost'):
        self.db = DataBase(
            user=user,
            password=pswd,
            name=name,
            host=host
        )
        self.business = self.db.get_business()
        self.owners = self.db.get_owners()
        self.suppliers = self.db.get_suppliers()
        self.ratings = self.db.get_ratings()
        self.set_data(self.BusinessTable, self.columns_business, self.business)
        self.set_data(self.ownersTable, self.columns_owners, self.owners)
        self.set_data(self.suppliersTable, self.columns_suppliers, self.suppliers)
        self.set_data(self.ratingsTable, self.columns_ratings, self.ratings)

    def drop_database(self):
        self.db.drop_database()
        self.connectWindow.show()

    def clear_all(self):
        self.db.delete_businesses()
        self.business = self.db.get_business()
        self.set_data(self.BusinessTable, self.columns_business, self.business)

        self.db.delete_owners()
        self.owners = self.db.get_owners()
        self.set_data(self.ownersTable, self.columns_owners, self.owners)

        self.db.delete_suppliers()
        self.suppliers = self.db.get_suppliers()
        self.set_data(self.suppliersTable, self.columns_suppliers, self.suppliers)

        self.db.delete_ratings()
        self.ratings = self.db.get_ratings()
        self.set_data(self.ratingsTable, self.columns_ratings, self.ratings)

    def set_data(self, table, columns, data):
        self.changed = True
        if data is not None:
            table.setRowCount(len(data))
            for i, row in enumerate(data):
                for j, col in enumerate(columns):
                    table.setItem(i, j, QTableWidgetItem(str(row[col])))
        else:
            table.setRowCount(0)
        self.changed = False

    # ----------------- Lounge bar functions --------------------
    def add_business(self):
        self.db.add_business(
            name=self.businessNameText.text(),
            address=self.addressText.text(),
            supplier=self.supplierText.text(),
            owner=self.ownerNameText_2.text(),
            feature=self.featureText.text()
        )
        self.business = self.db.get_business()
        self.set_data(self.BusinessTable, self.columns_business, self.business)
        self.businessNameText.clear()
        self.ownerNameText_2.clear()
        self.supplierText.clear()
        self.featureText.clear()
        self.addressText.clear()

    def delete_business(self):
        if len(self.BusinessTable.selectedIndexes()):
            for i in self.BusinessTable.selectedIndexes():
                self.db.delete_business(self.business[i.row()]['name'])
                self.business = self.db.get_business()
                self.set_data(self.BusinessTable, self.columns_business, self.business)

    def delete_businesses(self):
        self.db.delete_businesses()
        self.business = self.db.get_business()
        self.set_data(self.BusinessTable, self.columns_business, self.business)

    def search_business(self):
        if (self.businessNameText.text() == ''):
            self.business = self.db.get_business()
        else:
            self.business = self.db.search_business(self.businessNameText.text())
        self.set_data(self.BusinessTable, self.columns_business, self.business)

    def update_business(self, item):
        if not self.changed:
            self.db.update_business(item.text(), self.business[item.row()]['name'])
            self.business = self.db.get_business()
            self.set_data(self.BusinessTable, self.columns_business, self.business)
            self.ratings = self.db.get_ratings()
            self.set_data(self.ratingsTable, self.columns_ratings, self.ratings)

    # --------------------- Owner functions -----------------------
    def add_owner(self):
        self.db.add_owner(
            owner_name=self.ownerNameText.text(),
            f_date=self.foundationDate.text(),
            email=self.emailText.text()
        )
        self.owners = self.db.get_owners()
        self.set_data(self.ownersTable, self.columns_owners, self.owners)
        self.ownerNameText.clear()
        self.emailText.clear()

    def delete_owner(self):
        if len(self.ownersTable.selectedIndexes()):
            for i in self.ownersTable.selectedIndexes():
                self.db.delete_owner(self.owners[i.row()]['name'])
                self.owners = self.db.get_owners()
                self.set_data(self.ownersTable, self.columns_owners, self.owners)

    def delete_owners(self):
        self.db.delete_owners()
        self.owners = self.db.get_owners()
        self.set_data(self.ownersTable, self.columns_owners, self.owners)

    def search_owner(self):
        if (self.emailText.text() == ''):
            self.owners = self.db.get_owners()
        else:
            self.owners = self.db.search_owner(self.emailText.text())
        self.set_data(self.ownersTable, self.columns_owners, self.owners)

    def update_owner(self, item):
        if not self.changed:
            self.db.update_owner(item.text(), self.owners[item.row()]['name'])
            self.owners = self.db.get_owners()
            self.set_data(self.ownersTable, self.columns_owners, self.owners)
            self.business = self.db.get_business()
            self.set_data(self.BusinessTable, self.columns_business, self.business)

    # --------------------- Supplier functions -----------------------
    def add_supplier(self):
        self.db.add_supplier(
            organisation=self.organisationText.text(),
            reviews=self.reviewsText.text(),
            phone_number=self.phoneNumberText.text()
        )
        self.suppliers = self.db.get_suppliers()
        self.set_data(self.suppliersTable, self.columns_suppliers, self.suppliers)
        self.organisationText.clear()
        self.reviewsText.clear()
        self.phoneNumberText.clear()

    def delete_supplier(self):
        if len(self.suppliersTable.selectedIndexes()):
            for i in self.suppliersTable.selectedIndexes():
                self.db.delete_supplier(self.suppliers[i.row()]['organisation'])
                self.suppliers = self.db.get_suppliers()
                self.set_data(self.suppliersTable, self.columns_suppliers, self.suppliers)

    def delete_suppliers(self):
        self.db.delete_suppliers()
        self.suppliers = self.db.get_suppliers()
        self.set_data(self.suppliersTable, self.columns_suppliers, self.suppliers)

    def search_supplier(self):
        if self.phoneNumberText.text() == '':
            self.suppliers = self.db.get_suppliers()
        else:
            self.suppliers = self.db.search_supplier(self.phoneNumberText.text())
        self.set_data(self.suppliersTable, self.columns_suppliers, self.suppliers)

    def update_supplier(self, item):
        if not self.changed:
            self.db.update_supplier(item.text(), self.suppliers[item.row()]['organisation'])
            self.suppliers = self.db.get_suppliers()
            self.set_data(self.suppliersTable, self.columns_suppliers, self.suppliers)
            self.business = self.db.get_business()
            self.set_data(self.BusinessTable, self.columns_business, self.business)

    # --------------------- Ratings functions -----------------------
    def add_rating(self):
        self.db.add_rating(
            business_name=self.BusinessRatingsText.text(),
            feedback=self.feedbackText.text(),
            grade=int(self.gradeText.text())
        )
        self.ratings = self.db.get_ratings()
        self.set_data(self.ratingsTable, self.columns_ratings, self.ratings)
        self.BusinessRatingsText.clear()
        self.feedbackText.clear()
        self.gradeText.clear()

    def delete_rating(self):
        if len(self.ratingsTable.selectedIndexes()):
            for i in self.ratingsTable.selectedIndexes():
                self.db.delete_rating(self.ratings[i.row()]['business_name'])
                self.ratings = self.db.get_ratings()
                self.set_data(self.ratingsTable, self.columns_ratings, self.ratings)

    def delete_ratings(self):
        self.db.delete_ratings()
        self.ratings = self.db.get_ratings()
        self.set_data(self.ratingsTable, self.columns_ratings, self.ratings)

    def search_ratings(self):
        if self.BusinessRatingsText.text() == '':
            self.ratings = self.db.get_ratings()
        else:
            self.ratings = self.db.search_ratings(self.BusinessRatingsText.text())
        self.set_data(self.ratingsTable, self.columns_ratings, self.ratings)

    def update_ratings(self, item):
        if not self.changed:
            self.db.update_ratings(item.text(), self.ratings[item.row()]['business_name'])
            self.ratings = self.db.get_ratings()
            self.set_data(self.ratingsTable, self.columns_ratings, self.ratings)