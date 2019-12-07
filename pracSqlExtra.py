import sqlite3


def showReport(selected_menu, db, value):
    try:
        with (sqlite3.connect(db)) as conn:
            conn.row_factory = sqlite3.Row
            sql_command = sql_select(selected_menu, value)
            cursor = conn.execute(sql_command)

            if selected_menu == 1:
                found = len(conn.execute(sql_command).fetchall())
                print("Found {} Record(s)".format(found))
                for x, i in enumerate(cursor):
                    print("{:>2}.) {:40} : {:8.2f} Baht".format(x + 1, i["productname"], i["unitprice"]))

            elif selected_menu == 2:
                found = len(conn.execute(sql_command).fetchall())
                print("{} Found {} Record(s)".format(value["CategoryName"], found))
                for x, i in enumerate(cursor):
                    print("{:>2}.) {:40} : {:8.2f} Baht".format(x + 1, i["productname"], i["unitprice"]))

            elif selected_menu == 3:
                print("{:20} {}".format("Supplier From", " No.of Company"))
                print("-" * 35)
                for y in cursor:
                    print("{:25} {}".format(y["Country"], y["count(Country)"]))

            elif selected_menu == 4:
                print("Show Customers by Region")
                print("-" * 35)
                print("{:20} {:10} {:5}".format("Region", "Country", "City"))
                print("-" * 35)
                for y in cursor:
                    print("{:15} {:10} {:9}".format(y["Region"], y["countcountries"], y["countcities"]))

            elif selected_menu == 5:
                for y in cursor:
                    print("ID = {}".format(y["ProductId"]))
                    print("PRODUCT NAME = {}".format(y["ProductName"]))
                    print("STOCK VALUE = {:.2f}".format(y["stockvalue"]))
                    print("-" * 35)

            elif selected_menu == 6:
                found = len(conn.execute(sql_command).fetchall())
                print("Found {} Category(s)".format(found))
                for x, y in enumerate(cursor):
                    print("{:>2}.) {:20} {} PD. {:>10,.2f} Baht".format(x + 1, y["CategoryName"], y["numofproducts"],
                                                                        y["valueofstock"]))

            elif selected_menu == 7:
                for x, y in enumerate(cursor):
                    print("{:>2}.) {:40} {:>3}".format(x + 1, y["employeeName"], y["countOrders"]))

            elif selected_menu == 8:
                for y in cursor:
                    print("{} ({}) No. of Product = {} (Average price = {:.2f})".format(y["CompanyName"],
                                                                                        y["CategoryName"],
                                                                                        y["noofproduct"],
                                                                                        y["averageprice"]))

            elif selected_menu == 9:
                order_data = conn.execute(sql_command).fetchone()

                print("Order ID     : {}".format(order_data["OrderId"]))
                print("Order Date   : {}".format(order_data["OrderDate"]))
                print("Customer     : {}".format(order_data["ShipName"]))
                print("-" * 40)
                total_price = 0
                for x, y in enumerate(cursor):
                    print("{}.) {:35} {:>10,.2f}".format(x + 1, y["ProductName"], y["value"]))
                    total_price += y["value"]
                print("-" * 40)
                vat = total_price * (7 / 100)
                net_price = vat + total_price
                print("{:23} {:3} {:>9,.2f}".format("", "TOTAL PRICE\t:\t", total_price))
                print("{:23} {:3} {:>9,.2f}".format("", "VAT (7%)\t:\t", vat))
                print("{:23} {:3} {:>9,.2f}".format("", "NET PRICE\t:\t", net_price))
                print("-" * 40)
                print("Send By : {}".format(order_data["CompanyName"]))

            elif selected_menu == 10:
                print("Show Customers by Sales")
                print("-" * 50)
                print("{:15} {:15} {:15} {:15}".format("Country", "No.Of Order", "NET Price", "Price/Order"))
                print("-" * 50)
                for x in cursor:
                    print("{:15}\t{:>10} {:>15,.2f} {:>15,.2f}".format(x["ShipCountry"], x["nooforder"], x["netprice"], x["priceperorder"]))

    except Exception as e:
        print("Error {}".format(e))


def sql_select(selected_menu, value):
    sql_str = ""
    if selected_menu == 1:
        sql_str = """SELECT ProductName, UnitPrice
            FROM products
            WHERE UnitPrice Between {} and {}
            ORDER BY UnitPrice {};""".format(value["start_price"], value["end_price"],
                                             sort_selection(value["sort_option"]))

    elif selected_menu == 2:
        sql_str = """SELECT p.ProductName, p.UnitPrice
        FROM Products p JOIN Categories c ON p.CategoryId = c.CategoryId
        WHERE lower(c.CategoryName) = '{}'
        ORDER BY p.ProductName;""".format(value["CategoryName"].lower())

    elif selected_menu == 3:
        sql_str = """SELECT Country, count(Country)
        FROM Suppliers 
        GROUP BY Country 
        ORDER BY count(Country) desc"""

    elif selected_menu == 4:
        sql_str = """SELECT Region, count(DISTINCT Country) countcountries, count(DISTINCT City) countcities
        FROM Customers
        GROUP BY Region
        ORDER BY 3 desc;"""

    elif selected_menu == 5:
        sql_str = """SELECT ProductId, ProductName, UnitPrice * UnitsInStock as stockvalue 
        FROM products 
        WHERE stockvalue > {} 
        ORDER BY stockvalue desc""".format(value["my_stock_value"])

    elif selected_menu == 6:
        sql_str = """SELECT c.CategoryName, count(p.ProductName) as numofproducts, sum(UnitPrice * UnitsInStock) valueofstock
        FROM Categories c
        JOIN Products p ON c.CategoryId = p.CategoryId
        GROUP BY c.CategoryName
        HAVING valueofstock > {}
        ORDER BY valueofstock;""".format(value["valueStock"])

    elif selected_menu == 7:
        sql_str = """SELECT e.FirstName || " " || e.LastName || " , " || e.TitleOfCourtesy employeeName,
        count(o.OrderId) as countOrders
        FROM Orders o
        JOIN Employees e ON e.EmployeeId = o.EmployeeId
        GROUP BY employeeName
        ORDER BY countOrders;"""

    elif selected_menu == 8:
        sql_str = """SELECT s.CompanyName, c.CategoryName, count(p.ProductName) noofproduct, 
        avg(UnitPrice) as averageprice
        FROM Products p
        JOIN Categories c ON p.CategoryId = c.CategoryId
        JOIN Suppliers s ON p.SupplierId = s.SupplierId
        GROUP BY s.SupplierId, c.CategoryId
        ORDER BY CompanyName"""

    elif selected_menu == 9:
        sql_str = """SELECT o.OrderId, o.OrderDate, o.ShipName, p.ProductName, s.CompanyName, d.UnitPrice * d.Quantity value
        FROM Orders o
        JOIN OrdersDetails d ON o.OrderId = d.OrderId
        JOIN Shippers s ON o.ShipVia = s.ShipperID
        JOIN Products p ON d.ProductId = p.ProductId
        WHERE o.OrderId = {}
		ORDER BY p.ProductName"""\
            .format(value["orderId"])

    elif selected_menu == 10:
        sql_str = """SELECT o.ShipCountry, count(d.OrderId) nooforder, sum(d.UnitPrice * d.Quantity) - ((sum(d.UnitPrice * d.Quantity) * d.Discount) / 100) netprice, 
        sum(d.UnitPrice * d.Quantity) / count(d.OrderId) as priceperorder
        FROM Orders o
        JOIN OrdersDetails d ON o.OrderId = d.OrderId
        JOIN Customers c ON o.CustomerId = c.CustomerId
        GROUP BY  c.Country
        ORDER BY priceperorder desc;"""

    return sql_str


def sort_selection(sort_num):
    if sort_num == 1:
        return 'asc'

    elif sort_num == 2:
        return 'desc'


if __name__ == '__main__':
    myDatabase = "AppData/Sqlite_Northwind.sqlite3"
    more_than = True

    menu = int(input("Enter menu what do you want : "))

    # pracSqlExtra1
    if menu == 1:
        while more_than:

            start_price = int(input("Enter start price you want to see : "))
            end_price = int(input("Enter end price you want to see : "))

            if end_price > start_price:
                more_than = False
                print("Sort price : [1] Ascending [2] Descending")
                sort_option = int(input("Select [1] or [2] : "))
                showReport(menu, myDatabase, {"start_price": start_price, "end_price": end_price, "sort_option": sort_option})

            else:
                print(">> End price should be more than start price <<")

    # pracSqlExtra2
    elif menu == 2:
        category = input("Enter your category name to see : ")
        showReport(menu, myDatabase, {"CategoryName": category})

    # pracSqlExtra3
    elif menu == 3:
        showReport(menu, myDatabase, 0)

    # pracSqlExtra4
    elif menu == 4:
        showReport(menu, myDatabase, 0)

    # pracSqlExtra5
    elif menu == 5:
        my_stock_value = input("Enter stock value more than : ")
        showReport(menu, myDatabase, {"my_stock_value": my_stock_value})

    # pracSqlExtra6
    elif menu == 6:
        value_of_stock = input("See Value of Stock bt Category >:")
        showReport(menu, myDatabase, {"valueStock": value_of_stock})

    # pracSqlExtra7
    elif menu == 7:
        showReport(menu, myDatabase, 0)

    # pracSqlExtra8
    elif menu == 8:
        showReport(menu, myDatabase, 0)

    elif menu == 9:
        order_id = int(input("กรุณากรอก Order ID ที่ต้องการดูข้อมูล : "))
        showReport(menu, myDatabase, {"orderId": order_id})

    elif menu == 10:
        showReport(menu, myDatabase, 0)