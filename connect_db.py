import mysql.connector
my = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
)
my_cursor = my.cursor()
my_cursor.execute("CREATE DATABASE Blog_flask")
my_cursor.execute("SHOW DATABASES")
for db in my_cursor:
    print(db)