from db import get_connection
conn = get_connection()
cursor = conn.cursor()
from datetime import datetime
class admin:
    def __init__(self, name, CNIC):
        self.name = name
        self.CNIC = CNIC
    
    def register_employee(self):
        now = datetime.now().strftime("%Y-%m-%d")
        sql = """
        INSERT INTO emp_info(name, CNIC, Registeration_Date)
        VALUES(%s, %s, %s)
        """
        values = (self.name, self.CNIC, now)

        cursor.execute(sql, values)
        conn.commit()
        return f"{self.name} is registered successfully"
    def employee_fetchall(self):

        sql = """SELECT * FROM emp_info where CNIC = %s"""
        values = (self.CNIC, )
        cursor.execute(sql, values)
        data = cursor.fetchall()
        if data:
           return data
        else:
            return f"there is no data for this {self.cnic} CNIC "
