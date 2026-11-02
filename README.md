# Employee Management System

A web-based Employee Management System developed using **Python and Django**. This application helps manage employees, departments, roles, and users through a dashboard with role-based access control.

## Features

- **Dashboard** – Main page of the application.
- **Employee Management** – Add, view, edit, and delete employees.
- **Department Management** – Manage company departments.
- **Role Management** – Create and manage employee roles.
- **User Management** – Add, view, edit, and delete users.
- **Authentication** – Login, logout, and registration.
- **Role-Based Access Control** – Control access according to user roles.
- **Django Admin** – Administrative interface.

## Technologies Used

- Python
- Django
- SQLite3
- HTML5
- CSS3
- Bootstrap
- JavaScript

## Project URLs

| Page | URL |
|---|---|
| Login | `http://127.0.0.1:8000/login/` |
| Dashboard (Main Page) | `http://127.0.0.1:8000/dashboard/` |
| Logout | `http://127.0.0.1:8000/logout/` |
| Django Admin | `http://127.0.0.1:8000/admin/` |

## Demo Login Credentials

**Password for the demo accounts:** `123456`

| Username | Role | Password |
|---|---|---|
| cp | Admin | 123456 |
| SuperAdmin | Admin | 123456 |
| cp | To be confirmed | 123456 |

*Note: These are local demo credentials. Replace them with secure credentials and never use these passwords in production.*

## Installation and Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/dhvanimakadia/emp_app.git
   ```

2. Navigate to the project directory:

   ```bash
   cd employee_management
   ```

3. Create a virtual environment:

   ```bash
   python -m venv env
   ```

4. Activate the virtual environment:

   ```bash
   env\Scripts\activate
   ```

5. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

6. Apply database migrations:

   ```bash
   python manage.py migrate
   ```

7. Run the development server:

   ```bash
   python manage.py runserver
   ```

8. Open your browser:

   ```text
   http://127.0.0.1:8000/
   ```

# Author

**Dhvani Makadia**

B.Tech – Information Technology
