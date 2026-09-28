
"""
API.py - ONLY API PART - Works with your ORIGINAL 5 files without changing them
- Imports db.py, employer.py, employee.py
- Does NOT change them
- main_admin.py and main_employee.py are not used (replaced by browser)
"""
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from datetime import date
from db import connection, cursor
from employer import admin
from employee import Employee

app = FastAPI(title="Employee Payroll - Modular API")

class EmployeeCreate(BaseModel):
    name: str
    CNIC: str

class HoursCreate(BaseModel):
    CNIC: str
    hours: int
    work_date: date = date.today()

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
def home():
    return page("Payroll - Using Your Original Files", """
    <p>Your original files <b>employee.py, employer.py, db.py, input.py</b> are untouched.</p>
    <p>This API.py only imports them.</p>
    <p><a href="/admin"><button>Admin Panel (employer.py)</button></a></p>
    <p><a href="/employee"><button>Employee Panel (employee.py)</button></a></p>
    """)

# ---- ADMIN ----
@app.get("/admin", response_class=HTMLResponse)
def admin_panel():
    return page("Admin - employer.py", """
    <h3>Register Employee</h3>
    <form method="post" action="/admin/register-form">
        <input name="name" placeholder="Name" required>
        <input name="cnic" placeholder="13 digit CNIC" required>
        <button type="submit">Register</button>
    </form><hr>
    <h3>Get Employee Info</h3>
    <form method="get" action="/admin/employee-view">
        <input name="cnic" placeholder="CNIC" required>
        <button type="submit">Get Info</button>
    </form>
    """)

@app.post("/admin/register-form", response_class=HTMLResponse)
def register_form(name: str = Form(...), cnic: str = Form(...)):
    cnic = cnic.replace("-", "").strip()
    if len(cnic)!=13 or not cnic.isdigit():
        return page("Error", "CNIC must be 13 digits")
    # Check duplicate using db (original employer.py doesn't check)
    cursor.execute("SELECT * FROM emp_info WHERE CNIC=%s", (cnic,))
    if cursor.fetchone():
        return page("Error", f"CNIC {cnic} already registered")
    # Use your ORIGINAL admin class
    emp = admin(name, cnic)
    result = emp.register_employee()
    return page("Success", f"<p style='color:green'>{result}</p>")

@app.get("/admin/employee-view", response_class=HTMLResponse)
def employee_view(cnic: str):
    cnic = cnic.replace("-", "").strip()
    emp = admin("", cnic)
    data = emp.employee_fetchall()  # uses your original employer.py
    return page("Employee Info", f"<pre>{data if data else 'Not found'}</pre>")

# ---- EMPLOYEE ----
@app.get("/employee", response_class=HTMLResponse)
def employee_panel():
    today = date.today().isoformat()
    return page("Employee - employee.py", f"""
    <h3>Log Hours</h3>
    <form method="post" action="/employee/log-hours-form">
        <input name="cnic" placeholder="CNIC" required>
        <input name="hours" type="number" min="0" max="24" placeholder="Hours" required>
        <input name="work_date" type="date" value="{today}" required>
        <button type="submit">Log Hours</button>
    </form><hr>
    <h3>Calculate Salary</h3>
    <form method="get" action="/employee/salary-view">
        <input name="cnic" placeholder="CNIC" required>
        <input name="rate" type="number" placeholder="Hourly rate" required>
        <button type="submit">Calculate</button>
    </form><hr>
    <h3>Get Hours</h3>
    <form method="get" action="/employee/hours-view">
        <input name="cnic" placeholder="CNIC" required>
        <button type="submit">Get Hours</button>
    </form>
    """)

@app.post("/employee/log-hours-form", response_class=HTMLResponse)
def log_form(cnic: str = Form(...), hours: int = Form(...), work_date: str = Form(...)):
    cnic = cnic.replace("-", "").strip()
    # Use employee_id() from your original employee.py
    try:
        emp = Employee("", cnic)
        emp_id = emp.employee_id()
    except:
        return page("Error", f"CNIC {cnic} not registered")
    # Then insert (original log_hours() uses input(), so we do direct insert here)
    cursor.execute("INSERT INTO work_hours(employee_id, work_date, hours_worked) VALUES(%s,%s,%s)", (emp_id, work_date, hours))
    connection.commit()
    return page("Logged", f"You have logged {hours} hours on {work_date} for {cnic}")

@app.get("/employee/hours-view", response_class=HTMLResponse)
def hours_view(cnic: str):
    cnic = cnic.replace("-", "").strip()
    emp = Employee("", cnic)
    try:
        data = emp.get_hours_worked()  # uses your original employee.py
    except:
        return page("Error", "CNIC not registered")
    return page("Hours", f"<pre>{data if data else 'No hours'}</pre>")

@app.get("/employee/salary-view", response_class=HTMLResponse)
def salary_view(cnic: str, rate: int):
    cnic = cnic.replace("-", "").strip()
    emp = Employee("", cnic)
    try:
        emp_id = emp.employee_id()
    except:
        return page("Error", f"CNIC {cnic} not registered")
    cursor.execute("SELECT SUM(hours_worked) FROM work_hours WHERE employee_id=%s", (emp_id,))
    total = cursor.fetchone()[0]
    if not total:
        return page("No Hours", f"No hours found for {cnic}")
    salary = total * rate
    return page("Salary", f"<p>Your salary is: <b>{salary} Rupees</b> for {total} hours at rate {rate}</p>")

# JSON API (for /docs)
@app.post("/admin/register")
def api_register(data: EmployeeCreate):
    return register_form(data.name, data.CNIC)

@app.get("/admin/employees")
def get_all():
    cursor.execute("SELECT * FROM emp_info")
    return cursor.fetchall()
