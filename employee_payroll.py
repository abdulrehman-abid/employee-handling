"""======================================================= employee payroll============================================================"""
"""============================ Collecting Raw Data ============================"""
from datetime import datetime
now = datetime.now().strftime("%Y-%m-%d")

from getpass import getpass
import mysql.connector

"""===================== Database ======================="""
password = getpass("Enter your password of database: ")
connection = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = password,
    database = "employees"
)

cursor = connection.cursor()
"""======================= Engine ======================="""

def find_employee_CNIC():
    while True:
        try:
            employee_CNIC = input("Enter your CNIC: ").replace("-", "").strip()
        
            if len(employee_CNIC) != 13 or not employee_CNIC.isdigit():
                print("Invalid CNIC OR It should be 13 digits long.")
                continue
            else:
                cursor.execute("SELECT * FROM emp_info where CNIC = %s",(employee_CNIC, ))
                data = cursor.fetchone()

                if not data:
                    print("This CNIC is not registered.")
                    continue

                return employee_CNIC

        except ValueError:
            print("Invalid input. Please enter a valid CNIC number.")

def get_new_CNIC():
    while True:
            try:
                employee_CNIC = input("Enter your CNIC: ").replace("-", "").strip()
        
                if len(employee_CNIC) != 13 or not employee_CNIC.isdigit():
                    print( "Invalid CNIC. It should be 13 digits long.")
                    continue
                else:
                    cursor.execute("SELECT * FROM emp_info where CNIC = %s",(employee_CNIC, ))
                    data = cursor.fetchone()

                    if data :
                        print("This CNIC is already registered.")
                        continue

                    return employee_CNIC

            except ValueError:
                print("Invalid input. Please enter a valid CNIC number.")
def name():
    return input("Enter your name: ").strip()

class Employee:
    def __init__(self, name, CNIC):
        self.name = name
        self.CNIC = CNIC

    def employee_id(self):
        sql = """SELECT id FROM emp_info WHERE CNIC = %s"""
        values = (self.CNIC, )
        cursor.execute(sql, values)
        data = cursor.fetchone()[0]
        return data
 
    def register_employee(self):
        sql = """
        INSERT INTO emp_info(name, CNIC)
        VALUES(%s, %s)
        """
        values = (self.name, self.CNIC)

        cursor.execute(sql, values)
        connection.commit()
        return f"{self.name} is registered successfully"

    
    def calculate_salary(self):
        search_CNIC = self.CNIC
        total_hours = 0
        

             
        cursor.execute("SELECT sum(hours_worked) FROM work_hours where employee_id = %s",(self.employee_id(), ))
        total_hours = cursor.fetchone()[0]
        if not total_hours :
            return f"No hours found for this CNIC: {search_CNIC}"

        else:
            rate = int(input("Enter the hourly rate: "))
            salary = total_hours * rate
            return f"Your salary is: {salary} Rupees for {total_hours} hours"
    
    def __repr__(self):
        return (f"Salary Calculator: {self.calculate_salary()}")



    def log_hours(self):
        
        while True:
            try:
                hours = int (input("Enter the hours worked today:"))
            except ValueError:
                print("Invalid input. Please enter a valid number.")
                continue
            if hours < 0 or hours > 24:
                print("Invalid input. Please enter a number between 0 and 24.")
                continue
            else:
                sql = """SELECT id FROM emp_info WHERE CNIC = %s"""
                values = (self.CNIC, )
                cursor.execute(sql, values)
                data = cursor.fetchone()[0]


                sql = """INSERT INTO work_hours(employee_id, work_date, hours_worked)
                VALUES(%s, %s, %s)"""
                values = (data, now, hours)
                cursor.execute(sql, values)
                connection.commit()
                return f"You have logged {hours} hours"


    def employee_fetchall(self):

        sql = """SELECT * FROM emp_info where CNIC = %s"""
        values = (self.CNIC, )
        cursor.execute(sql, values)
        data = cursor.fetchall()
        return data
    
    def get_hours_worked(self):
        sql = """SELECT * FROM work_hours where employee_id = %s"""
        values = (self.employee_id(), )
        cursor.execute(sql, values, )
        data = cursor.fetchall()
        return data

"""======================= User Interface ======================="""

menu_options = [

    "Add a new employee",
    "Log hours",
    "Calculate salary",
    "Get employee info",
    "Get hours worked",
    "Exit"
]

print("\n================ Welcome to Salary Calculator ================")
print("Welcome to Salary Calculator")
menu_string = ""
for index, options in enumerate(menu_options, start=1):
    menu_string += (f"{index}. {options}\n")
n = len(menu_options)

while True:
    print(menu_string)
    try:
        user_input = int(input(f"Enter your choice(1-{n}): "))
    except ValueError:
        print(f"Invalid input. Please enter a number between 1 and {n}.")
        continue
    if user_input == 1:
        employee_name = name()
        employee_CNIC = get_new_CNIC()
        employee = Employee(employee_name, employee_CNIC)
        print(employee.register_employee())
    elif user_input == 2:
        employee_CNIC = find_employee_CNIC()
        employee = Employee("", employee_CNIC)
        print(employee.log_hours())
    elif user_input == 3:
        employee_CNIC = find_employee_CNIC()
        employee = Employee("", employee_CNIC)
        print(employee.calculate_salary())
    elif user_input == 4:
        employee_CNIC = find_employee_CNIC()
        employee = Employee("", employee_CNIC)
        print(employee.employee_fetchall())
    elif user_input == 5:
        employee_CNIC = find_employee_CNIC()
        employee = Employee("", employee_CNIC)
        print(employee.get_hours_worked())
    elif user_input == 6:
        print("Thank you for using Salary Calculator")

        # === CLOSE CONNECTIONS HERE ===
        cursor.close()
        connection.close()
        print("Database connection closed cleanly.")
        # ==============================

        break
    else:
        print(f"Invalid input. Please enter a number between 1 and {n}.")  