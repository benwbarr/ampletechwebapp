import mysql.connector

mydb = mysql.connector.connect(
    host="10.104.1.52",
    user="benwebwd",
    passwd = "w8TBX&MsZvC&F92Qc9Fa9c")

my_cursor = mydb.cursor()

#my_cursor.execute("CREATE DATABASE benwebwd")

my_cursor.execute("SHOW DATABASES")
for db in my_cursor:
    print(db)