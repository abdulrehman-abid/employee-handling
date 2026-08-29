"""======================= salary calculator ======================="""
"""======================= Imports ======================="""
from datetime import datetime
now = datetime.now().strftime("%y-%m-%d")

"""======================= Engine ======================="""

def CNIC_verify():
    while True:
            try:
                employee_CNIC = (input("Enter your CNIC: ")).replace("-", "").strip()
           
                if len(employee_CNIC) != 13 or not employee_CNIC.isdigit():
                    print( "Invalid CNIC. It should be 13 digits long.")
                    continue
                else:
                    data = open("data.txt", "r")
                    data.seek(0)  
                    data_content = data.read()
                    data.close()

                    if employee_CNIC in data_content:
                        print("This CNIC is already registered.")
                        continue
                    return employee_CNIC
            except ValueError:
                print("Invalid input. Please enter a valid CNIC number.")
def name():
    return input("Enter your name: ").strip() 

def register_employee():
    employee_name = name()
    employee_CNIC = CNIC_verify()
    with open("data.txt", "a")as data:
        data.write(f"{employee_name},{employee_CNIC}\n")
        data.close()

class salary_calculator():
    def __init__(self):
        self.salary = self.calculate_salary()

    def calculate_salary(self):
        search_CNIC = input("Enter your CNIC to calculate salary for: ").replace("-", "").strip()
        hours = []
        found = False

        try:        
            with open("log_hour.txt", "r") as file:
                file.seek(0)
                for line in file:
                    columns = line.strip().split(",")
                    if len(columns) == 3 and columns[1] == search_CNIC:
                            hours.append(int(columns[2]))
                            found = True
                rate = float(input("Enter the hourly rate: "))
                total_hours = sum(hours)
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
        self.employee_CNIC = self.employee_CNIC()
        self.log_hours = self.log_hours()

    def employee_CNIC(self):
        print("Enter CNIC to log hours")
        input_CNIC = input("Enter your CNIC: ")
        input_CNIC = input_CNIC.replace("-", "").strip()
        try:
            data_content = open("data.txt", "r").read()

            if input_CNIC  in data_content:
                return input_CNIC
            else:
                print("Invalid CNIC .OR register first")
        except FileNotFoundError:
            print("No data found.OR register first")

    def log_hours(self):
        if self.employee_CNIC != None:
            hours = int (input("Enter the hours worked today:"))
            if hours < 0 or hours > 24:
                print("Invalid input. Please enter a number between 0 and 24.")
            else:
                with open("log_hour.txt","a") as file:
                    file.write(f"{now},{self.employee_CNIC},{hours}\n")
                return f"You have logged {hours} hours"
        
"""======================= User Interface ======================="""


while True:
    print("\n================ Welcome to Salary Calculator ================")
    print("Welcome to Salary Calculator")
    print("1.Enter your name and CNIC to register.")
    print("2.Enter hours worked today, log hours")
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