import mysql.connector
from getpass import getpass

password = getpass("Enter your password of database: ")
connection = mysql.connector.connect(
    host = "localhost",
    user = "root",
    port = 3306,
    password = password,
    database = "employees"
)

cursor = connection.cursor()

print("connected successfully")