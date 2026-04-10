# Placement Portal

A Flask-based web application for managing campus placement workflows between students, companies, and administrators.

## Features

- Multi-role authentication: Admin, Company, Student
- Company onboarding with admin approval flow
- Student profile management with resume upload
- Placement drive creation, approval, and publishing
- Student application tracking per drive
- Company-side application status updates (Shortlisted/Selected/Rejected)
- Admin dashboard for students, companies, drives, and applications

## Tech Stack

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Bcrypt
- SQLite
- Jinja2 templates + static CSS

## Project Structure

```text
Placement_Portal/
	placement_portal/
		app.py
		models.py
		auth.py
		admin.py
		company.py
		student.py
		templates/
		static/
		instance/
```

## Prerequisites

- Python 3.10+
- `pip`

## Installation

1. Clone or open this project.
2. Create a virtual environment.
3. Install dependencies.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install flask flask-sqlalchemy flask-bcrypt
```

## Run the Application

From the project root:

```powershell
python placement_portal/app.py
```

Then open:

- http://127.0.0.1:5000

## Default Admin Login

On first run, the app auto-creates an admin account if none exists:

- Email: `admin@placement.com`
- Password: `admin123`

## User Flows

### Admin

- Log in to dashboard
- Approve/reject company registrations
- Blacklist/unblacklist students and companies
- Approve/reject/delete placement drives
- Manage students, companies, and applications

### Company

- Register account (await admin approval)
- Create and manage placement drives
- View applications per drive
- Update application status
- Manage company profile

### Student

- Register account and upload resume
- Browse approved open drives
- Apply to drives
- Track application statuses
- Manage personal profile

## Notes

- Database file is created automatically using SQLite.
- Resume uploads are stored under:
	- `placement_portal/static/uploads/resumes/`
- Max upload size is configured to 5 MB.

## Security Reminder

This project uses a hardcoded Flask secret key and default admin credentials for development convenience. Change them before production deployment.



