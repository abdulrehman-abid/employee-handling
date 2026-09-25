import mysql.connector
from getpass import getpass 
"""===================== Database ======================="""
password = getpass("Enter your password of database: ")
connection = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = password,
    database = "employees"
)

cursor = connection.cursor()