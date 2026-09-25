from db import connection, cursor
from datetime import datetime
now = datetime.now().strftime("%Y-%m-%d")

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
                now = datetime.now().strftime("%Y-%m-%d")
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


    def get_hours_worked(self):
        sql = """SELECT * FROM work_hours where employee_id = %s"""
        values = (self.employee_id(), )
        cursor.execute(sql, values, )
        data = cursor.fetchall()
        return data

