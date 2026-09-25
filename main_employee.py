from db import connection, cursor
from employee import Employee
from input import find_employee_CNIC
"""======================= User Interface ======================="""

menu_options = [

    
    "Log hours",
    "Calculate salary",
    "Get hours worked",
    "Exit"
]

print("\n================ Welcome to employee payroll ================")
print("Welcome to employee payroll")
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
       
        employee_CNIC = find_employee_CNIC()
        employee = Employee("", employee_CNIC)
        print(employee.log_hours())
    elif user_input == 2:
        employee_CNIC = find_employee_CNIC()
        employee = Employee("", employee_CNIC)
        print(employee.calculate_salary())
    elif user_input == 3:
        employee_CNIC = find_employee_CNIC()
        employee = Employee("", employee_CNIC)
        print(employee.get_hours_worked())
    elif user_input == n:
        print("Thank you for using Salary Calculator")

        # === CLOSE CONNECTIONS HERE ===
        cursor.close()
        connection.close()
        print("Database connection closed cleanly.")
        # ==============================

        break
    else:
        print(f"Invalid input. Please enter a number between 1 and {n}.")  