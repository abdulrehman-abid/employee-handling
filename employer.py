from db import get_connection
conn = get_connection()
cursor = conn.cursor()
from datetime import datetime
class admin:
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

    def delete_employee(self):
        sql ="""select name from emp_info where CNIC=%s"""
        values = (self.CNIC, )
        cursor.execute(sql, values)
        result = cursor.fetchone()
        if result:
            name = {result[0]}
        else:
            return "Employee not found"

        sql = """delete from emp_info where CNIC=%s"""
        values = (self.CNIC, )
        cursor.execute(sql, values)
        conn.commit()

        sql = """delete from work_hours where employee_id = %s"""
        values = (self.employee_id(), )
        cursor.execute(sql, values)
        conn.commit()

        return f"{name} is deleted completely from the database"

    def employee_fetchall(self):
        sql = """
        SELECT e.id, e.name, e.CNIC, COALESCE(SUM(w.hours_worked), 0) AS total_hours
        FROM emp_info e
        LEFT JOIN work_hours w ON w.employee_id = e.id
        GROUP BY e.id, e.name, e.CNIC
        ORDER BY e.id ASC
        """
        cursor.execute(sql)
        data = cursor.fetchall()

        if not data:
            return "<p>No employee found</p>"

        rows_html = "".join(
            f"<tr>"
            f"<td>{row[0]}</td>"
            f"<td>{row[1]}</td>"
            f"<td>{row[2]}</td>"
            f"<td>{row[3]:.1f} hrs</td>"
            f"</tr>"
            for row in data
        )

        return f"""
        <table border="1" cellpadding="8" cellspacing="0" style="border-collapse: collapse; font-family: sans-serif;">
            <thead style="background-color: #f2f2f2; text-align: left;">
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>CNIC</th>
                    <th>Total Hours</th>
                </tr>
            </thead>
            <tbody>
                {rows_html}
            </tbody>
        </table>
    """
    