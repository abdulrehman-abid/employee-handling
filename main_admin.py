from db import connection, cursor
from employer import admin

from input import get_new_CNIC, name, find_employee_CNIC

"""======================= User Interface ======================="""

menu_options = [


    "register employee",
    "Get employee info",
    "Exit"
]

print("\n================ Welcome to employee payroll (admin) ================")
print("Welcome to employee payroll")
menu_string = ""
for index, options in enumerate(menu_options, start=1):
    menu_string += (f"{index}. {options}\n")
n = len(menu_options)

while True:
    print(menu_string)
    try:
        user_input = int(input(f"Enter your choice(1-{n}): "))
    except ValueError or user_input < 1 or user_input > n:
        print(f"Invalid input. Please enter a number between 1 and {n}.")
        continue
    if user_input == 1:
        employee_name = name()
        employee_CNIC = get_new_CNIC()
        employee = admin(employee_name, employee_CNIC)
        print(employee.register_employee())
    elif user_input == 2:
        employee_CNIC = find_employee_CNIC()
        employee = admin("", employee_CNIC)
        print(employee.employee_fetchall())
    elif user_input == n:
        print("Thank you for using employee payroll")

        # === CLOSE CONNECTIONS HERE ===
        cursor.close()
        connection.close()
        print("Database connection closed cleanly.")
        # ==============================

        break