"""======================= salary calculator ======================="""
"""============================ Imports ============================"""
from datetime import datetime
now = datetime.now().strftime("%y-%m-%d")

"""===================== Database ======================="""
import mysql.connector

connection = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "my_password",
    database = "employees"
)

cursor = connection.cursor()
"""======================= Engine ======================="""
def find_employee_CNIC():
    while True:
                try:
                    employee_CNIC = (input("Enter your CNIC: ")).replace("-", "").strip()
               
                    if len(employee_CNIC) != 13 or not employee_CNIC.isdigit():
                        print( "Invalid CNIC OR It should be 13 digits long.")
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
                employee_CNIC = (input("Enter your CNIC: ")).replace("-", "").strip()
           
                if len(employee_CNIC) != 13 or not employee_CNIC.isdigit():
                    print( "Invalid CNIC. It should be 13 digits long.")
                    continue
                else:
                    cursor.execute("SELECT * FROM emp_info where CNIC = %s",(employee_CNIC, ))
                    data = cursor.fetchone()

                    if len(data) != 0:
                        print("This CNIC is already registered.")
                        continue

                    return employee_CNIC

            except ValueError:
                print("Invalid input. Please enter a valid CNIC number.")
def name():
    return input("Enter your name: ").strip() 

def register_employee():
    employee_name = name()
    employee_CNIC = get_new_CNIC()
    sql = """
    INSERT INTO emp_info(name, CNIC)
    VALUES(%s, %s)
    """
    values = (employee_name, employee_CNIC)

    cursor.execute(sql, values)
    connection.commit()

class salary_calculator():
    def __init__(self):
        self.salary = self.calculate_salary()

    def calculate_salary(self):
        search_CNIC = find_employee_CNIC()
        total_hours = 0
        found = False

        try:        
            cursor.execute("SELECT * FROM work_hours where CNIC = %s",(search_CNIC, ))
            data = cursor.fetchall()

            for row in data:
                total_hours += row[3]

            rate = float(input("Enter the hourly rate: "))
            salary = total_hours * rate
            return f"Your salary is: {salary} Rupees for {total_hours} hours"
                            
        except FileNotFoundError:
            print("No hours logged yet.Please log hours first.")  

        if not found :
            print(f"No hours found for this CNIC: {search_CNIC}")

        
        
    def __repr__(self):
        return (f"Salary Calculator: {self.salary}")

class log_daily_hours():
    def __init__ (self):
        self.is_registered = self.is_registered()
        self.log_hours = self.log_hours()

    def is_registered(self):
        find_employee_CNIC()

    def log_hours(self):
        if self.is_registered != None:
            hours = int (input("Enter the hours worked today:"))
            if hours < 0 or hours > 24:
                print("Invalid input. Please enter a number between 0 and 24.")
            else:
                sql = """SELECT id FROM emp_info WHERE CNIC = %s"""
                values = (self.is_registered, )
                cursor.execute(sql, values)
                data = cursor.fetchone()


                sql = """INSERT INTO work_hours(employee_id, work_date, hours_worked)
                VALUES(%s, %s, %s)"""
                values = (data, now, hours)
                cursor.execute(sql, values)
                connection.commit()
                return f"You have logged {hours} hours"
        
"""======================= User Interface ======================="""


while True:
    print("\n================ Welcome to Salary Calculator ================")
    print("Welcome to Salary Calculator")
    print("1.Add a new employee")
    print("2.Log hours")
    print("3.calculate salary")
    print("4.Exit")
    try:
        user_input = int(input("Enter your choice(1-4): "))
    except ValueError:
        print("Invalid input. Please enter a number between 1 and 4.")
        continue
    if user_input == 1:
        register_employee()
    elif user_input == 2:
        log_daily_hours()
    elif user_input == 3:
        print(salary_calculator())
    elif user_input == 4:
        print("Thank you for using Salary Calculator")
        break
    else:
        print("Invalid input. Please enter a number between 1 and 4.")