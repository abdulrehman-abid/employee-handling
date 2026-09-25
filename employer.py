from db import connection, cursor

class admin:
    def __init__(self, name, CNIC):
        self.name = name
        self.CNIC = CNIC
    
    def register_employee(self):
        sql = """
        INSERT INTO emp_info(name, CNIC)
        VALUES(%s, %s)
        """
        values = (self.name, self.CNIC)

        cursor.execute(sql, values)
        connection.commit()
        return f"{self.name} is registered successfully"
    def employee_fetchall(self):

        sql = """SELECT * FROM emp_info where CNIC = %s"""
        values = (self.CNIC, )
        cursor.execute(sql, values)
        data = cursor.fetchall()
        return data
    
