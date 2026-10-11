import mysql.connector
import time
from mysql.connector.errors import DatabaseError
import os
"""===================== Database ======================="""

def get_connection():
    # 2. Use os.getenv so it works locally and inside Docker automatically
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST", "db"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME", "employees")
    )
    return connection

"""===================== Create Tables ======================="""

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS emp_info (
            id int NOT NULL AUTO_INCREMENT,
            name varchar(20) NOT NULL,
            CNIC varchar(15) NOT NULL,
            Registeration_Date date DEFAULT NULL,
            PRIMARY KEY (id),
            UNIQUE KEY CNIC (CNIC)
        )
    """)
    conn.commit()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS work_hours (
        id INT AUTO_INCREMENT PRIMARY KEY,
        employee_id INT NOT NULL,
        work_date DATE NOT NULL,
        hours_worked INT NOT NULL,
        
        FOREIGN KEY (employee_id) 
            REFERENCES emp_info(id)
        )
        """)
    conn.commit()
    

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS work_hours_history (
    history_id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT,
    work_date DATE,
    hours_worked INT,
    archived_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (employee_id) REFERENCES emp_info(id)
    )""")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS salary_payments (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT,
    total_hours INT,
    hourly_rate INT,
    total_salary INT,
    paid_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (employee_id) REFERENCES emp_info(id)
    )
    """) 
    return "Tables created successfully"


def init_db():
    retries = 5
    while retries > 0:
        try:
            create_tables()
            print("Database tables created/verified successfully!")
            return
        except DatabaseError as e:
            retries -= 1
            print(f"Database not ready yet ({e}). Retrying in 2 seconds... ({retries} attempts left)")
            time.sleep(2)
    print("Could not connect to database during startup.")

# Run initialization safely
if __name__ != "__main__":
    init_db()
