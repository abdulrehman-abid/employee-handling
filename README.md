# Employee Handling System

A Python employee management and payroll system built as a learning project.

## Features

- Employee registration
- Employee deletion
- Employee information retrieval
- Working-hours tracking
- Salary calculation
- MySQL database
- FastAPI web interface
- JSON API

## Tech Stack

- Python
- FastAPI
- Pydantic
- MySQL
- HTML/CSS

## Project Structure

- `employee.py` - Employee operations
- `employer.py` - Admin/employer operations
- `API.py` - FastAPI application
- `db.py` - Database connection

## API

### Register employee

`POST /api/admin/register`

### Get employees

`GET /api/admin/employees`

### Get employee

`GET /api/employees/{cnic}`

### Get employee hours

`GET /api/employees/{cnic}/hours`

## Purpose

This project was built to practice Python OOP, MySQL, FastAPI,
HTTP APIs, and backend development.
