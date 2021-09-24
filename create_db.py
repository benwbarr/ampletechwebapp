import mysql.connector

mydb = mysql.connector.connect(
    host="10.104.1.52",
    user="benwebwd",
    passwd = "w8TBX&MsZvC&F92Qc9Fa9c",
    database ="wd")

my_cursor = mydb.cursor()

my_cursor.execute("CREATE TABLE Users (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), email VARCHAR(255) UNIQUE)")

my_cursor.execute("SHOW TABLE")
for x in my_cursor:
  print(x)