from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from db import get_connection
conn = get_connection()
from employee import Employee
from employer import admin
from datetime import date

app = FastAPI()

class EmployeeCreate(BaseModel):
    name : str
    CNIC : str

class AdminForm(BaseModel):
    name : str
    CNIC : str
    work_date : date = date.today()

def page(title, body):
    return f"""
    <html><head><title>{title}</title>
    <style>
    body{{font-family:Arial; background:#f0f2f5; padding:20px}}
        .box{{background:white; padding:20px; border-radius:10px; max-width:650px; margin:auto; box-shadow:0 2px 8px #ccc}}
        input{{padding:10px; margin:5px 0; width:95%}} button{{padding:10px 20px; background:#0d6efd; color:white; border:none; border-radius:5px; cursor:pointer}}
        a{{text-decoration:none}} pre{{background:#eee; padding:10px; border-radius:5px}}
        </style></head><body><div class="box"><h2>{title}</h2>{body}
        <br><br><a href="/">Home</a> | <a href="/admin">Admin</a> | <a href="/employee">Employee</a> | <a href="/docs">Docs</a>
        </div></body></html>
    """
@app.get("/", response_class=HTMLResponse)
def root():
    return page("employee payroll - Home page", """ 
    <p> This is an project designed to solve the problem of employee management</p>
    <p> The project is build in such a way so that it can be easily maintained</p>
    <p><a href="/admin"><button>Admin Panel</button></a></p>
    <p><a href="/employee"><button>Employee Panel</button></a></p>""")

@app.get("/admin", response_class=HTMLResponse)
def admin_panel():
    return page("Admin Panel", """
    <h3>Register Employee</h3>
    <form method="post" action="/admin/register-form">
        <input name="name" placeholder="Enter employee name" required>
        <input name="cnic" placeholder="Enter employee CNIC" required>
        <button type="submit">Register</button>
    </form><hr>
    <h3>Get Employee Info</h3>
    <form method="get" action="/admin/employee-view">
        <input name="cnic" placeholder="Enter CNIC" required>
        <button type="submit">Get Info</button>
    </form>
    """)

@app.post("/admin/register-form", response_class=HTMLResponse)
def register_employee(name:str = Form(...), cnic:str = Form(...)):
    cnic = cnic.replace("-", "").strip()
    if len(cnic)!=13 or not cnic.isdigit():
        return page("Error", "CNIC must be 13 digits and numeric")
    # Check duplicate using db (original employer.py doesn't check)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM emp_info WHERE CNIC=%s", (cnic,))
    if cursor.fetchone():
        return page("Error", f"CNIC {cnic} already registered")
    # Use your ORIGINAL admin class
    emp = admin(name, cnic)
    result = emp.register_employee()
    return page("Success", f"<p style='color:green'>{result}</p>")

@app.get("/admin/employee-view",response_class=HTMLResponse)
def employee_view(cnic:str):
    cnic = cnic.replace("-", "").strip()
    emp = admin("", cnic)
    data = emp.employee_fetchall()  # uses your original employer.py
    return page("Employee Info", f"<pre>{data if data else 'Not found'}</pre>")

@app.get("/employee", response_class=HTMLResponse)
def employee_panel():
    return page("Employee Panel","""
    <h3>Calculate Salary</h3>
    <form method="get" action="/employee/salary-view">
        <input name= "cnic" placeholder="Enter your CNIC" required>
        <input name= "rate" type="number" placeholder="Enter hourly rate" required>
        <button type="submit">Calculate Salary</button>
    </form>
    <hr>
    <h3>Log Hours</h3>
    <form method="post" action="/employee/log-hours-form">
        <input name= "cnic" placeholder="Enter your CNIC" required>
        <input name= "hours" type="number" min="0" max="24" placeholder="Enter hours worked today" required>
        <button type="submit">Log Hours</button>
    </form>
    <hr>
    <h3>Get Hours</h3>
    <form method="get" action="/employee/hours-view">
        <input name= "cnic" placeholder="Enter your CNIC" required>
        <button type="submit">Get Hours</button>
    </form>
    """)

@app.get("/employee/salary-view", response_class=HTMLResponse)
def salary_view(cnic:str, rate:int):
    cnic = cnic.replace("-", "").strip()
    emp = Employee("", cnic)
    data = emp.calculate_salary(rate)
    return page("Salary", f"<p>{data}</p>")

@app.get("/employee/hours-view", response_class=HTMLResponse)
def hours_view(cnic:str):
    cnic = cnic.replace("-", "").strip()
    emp = Employee("", cnic)
    data = emp.get_hours_worked()
    if not data:
        return page("Hours", "<p>No hours found</p>")
    return page("Hours", f"<p>{data}</p>")

@app.post("/employee/log-hours-form", response_class=HTMLResponse)
def log_hours(cnic:str = Form(...), hours:int = Form(...)):
    cnic = cnic.replace("-", "").strip()
    emp = Employee("", cnic)
    data = emp.log_hours(hours)
    return page("Logged", f"<p>{data}</p>")

# JSON API (for /docs)
@app.post("/admin/register")
def api_register(data: EmployeeCreate):
    return register_employee(data.name, data.CNIC)

@app.get("/admin/employees")
def get_all():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM emp_info")
    return cursor.fetchall()