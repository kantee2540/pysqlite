import sqlite3


def newCategories(db):
    try:
        category_name = input("Input your category : ")
        with(sqlite3.connect(db)) as conn:
            sql_command = """
            BEGIN;
            INSERT INTO Categories(CategoryName) 
            values ('{}');
            COMMIT;
            """.format(category_name)
            conn.executescript(sql_command)

    except Exception as e:
        print("Error {}".format(e))


def changeContactSupplier(db):
    try:
        supplier_id = input("Enter you supplier id : ")
        with (sqlite3.connect(db)) as conn:
            conn.row_factory = sqlite3.Row
            sql_command = """SELECT SupplierID, CompanyName
            FROM Suppliers
            WHERE SupplierID = {};""".format(supplier_id)
            data = conn.execute(sql_command).fetchone()
            print("Shipper ID : {}".format(data["SupplierID"]))
            print("Company Name : {}".format(data["CompanyName"]))
            edit = input("Do you want to edit Company Name? [y][n]: ").lower()

            if edit == "y":
                new_company_name = input("Enter your new company name : ")
                sql_command = """UPDATE Suppliers
                 SET CompanyName = '{}' 
                 WHERE SupplierID = {}""".format(new_company_name, supplier_id)
                conn.executescript(sql_command)
                print("OK, I updated yout company name.")
            else:
                print("OK, I won't change your company name.")

    except Exception as e:
        print("Error {}".format(e))


def delOrderID(db):
    try:
        order_id = input("Input your orderID that want to delete : ")
        with (sqlite3.connect(db)) as conn:
            conn.row_factory = sqlite3.Row
            sql_command = """SELECT OrderID, ShipName
            FROM Orders
            WHERE OrderID = {};""".format(order_id)
            data = conn.execute(sql_command).fetchone()
            print("OrderID : {}".format(data["OrderID"]))
            print("ShipName : {}".format(data["ShipName"]))
            del_edit = input("Do you want to delete this OrderID? [y][n] : ").lower()
            if del_edit == "y":
                sql_command = "DELETE FROM Orders WHERE OrderID = {}".format(order_id)
                conn.executescript(sql_command)
                print("OK, I deleted your orderID")

            else:
                print("OK, I won't delete your orderID.")

            # sql_command = "DELETE FROM Orders WHERE OrderID = ?"

    except Exception as e:
        print("Error {}".format(e))


def genDatabase(db):
    sql = """CREATE TABLE `student`
     ( `ID` INTEGER PRIMARY KEY AUTOINCREMENT, `NAME` TEXT UNIQUE, `LASTNAME` TEXT, `GENDER` TEXT )"""


if __name__ == '__main__':
    myDatabase = "AppData/Sqlite_Northwind.sqlite3"
    # changeContactSupplier(myDatabase)
    delOrderID(myDatabase)
