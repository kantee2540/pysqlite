import sqlite3


def showReport(db, num):
    try:
        with (sqlite3.connect(db)) as conn:
            # Can define column in table
            conn.row_factory = sqlite3.Row
            # Triple quote
            sql_command = """SELECT 
            * FROM products
            WHERE unitprice > ?
            ORDER BY unitprice desc;"""
            cursor = conn.execute(sql_command, [num])
            for x, i in enumerate(cursor):
                print("({}) {} - {} - {}".format(x, i["productid"], i["productname"], i["unitprice"]))

    except Exception as e:
        print("Error {}".format(e))


if __name__ == '__main__':
    myDatabase = "AppData/Sqlite_Northwind.sqlite3"
    showReport(myDatabase, 30)
