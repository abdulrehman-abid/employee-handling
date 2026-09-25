from db import cursor
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
    name = input("Enter your name: ").strip()
    return name