from db import get_connection
conn = get_connection()
cursor = conn.cursor()
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
        data = cursor.fetchone()
        if data == None:
            return None
        return data[0]
    
    def calculate_salary(self, rate):
        total_hours = 0
        
        cursor.execute("SELECT sum(hours_worked) FROM work_hours where employee_id = %s",(self.employee_id(), ))
        total_hours = cursor.fetchone()
        if not total_hours or total_hours[0] is None:
            return f"No hours found for this CNIC: {self.CNIC}"

        else:
            total_hours = total_hours[0]
            salary = total_hours * rate
            return f"Your salary is: {salary} Rupees for {total_hours} hours"
    
    def __repr__(self):
        return f"Employee(name={self.name}, CNIC={self.CNIC})"



    def log_hours(self, hours):
        
        now = datetime.now().strftime("%Y-%m-%d")
        data = self.employee_id()
        if not data:
            return "CNIC not registered"

        sql = """INSERT INTO work_hours(employee_id, work_date, hours_worked)
        VALUES(%s, %s, %s)"""
        values = (data, now, hours)
        cursor.execute(sql, values)
        conn.commit()
        return f"You have logged {hours} hours"


    def get_hours_worked(self):
        sql = """SELECT * FROM work_hours where employee_id = %s"""
        employee_id = self.employee_id()
        if not employee_id:
            return "CNIC not registered"
        values = (employee_id, )
        cursor.execute(sql, values)
        raw_data = cursor.fetchall()
        if not raw_data:
            return "No hours found"
        data = []
        for lines in raw_data:
            data.append(f"Date: {lines[2]} | Hours Worked: {lines[3]}")
        return "<br>".join(data)
