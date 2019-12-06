import sqlite3


def showReport(db, sql):
    try:
        with (sqlite3.connect(db)) as conn:
            conn.row_factory = sqlite3.Row
            sql_command = sql
            found = len(conn.execute(sql_command).fetchall())
            cursor = conn.execute(sql_command)
            print("Found {} Record(s)".format(found))

            display(cursor)

    except Exception as e:
        print("Error {}".format(e))


def sql_command(menu, db, *value):
    sql_str = ""
    if menu == 1:
        sql_str = """SELECT ProductName, UnitPrice
            FROM products
            WHERE UnitPrice Between {} and {}
            ORDER BY UnitPrice {};""".format(value[0], value[1], sort_selection(value[2]))

    elif menu == 2:
        sql_str = """SELECT Pro
        """

    showReport(db, sql_str)


def display(cursor):
    for x, i in enumerate(cursor):
        print("{:>2}.) {:40} : {:8.2f} Baht".format(x + 1, i["productname"], i["unitprice"]))


def sort_selection(sort_num):
    if sort_num == 1:
        return 'asc'

    elif sort_num == 2:
        return 'desc'


if __name__ == '__main__':
    myDatabase = "AppData/Sqlite_Northwind.sqlite3"
    more_than = True

    menu = int(input("Enter menu what do you want : "))
    if menu == 1:
        while more_than:

            start_price = int(input("Enter start price you want to see : "))
            end_price = int(input("Enter end price you want to see : "))

            if end_price > start_price:
                more_than = False
                print("Sort price : [1] Ascending [2] Descending")
                sort_option = int(input("Select [1] or [2] : "))
                sql_command(myDatabase, start_price, end_price, sort_option)

            else:
                print(">> End price should be more than start price <<")

    elif menu == 2:
        category = input("Enter your category name to see : ")
