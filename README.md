# PlacementHub - Placement Portal Application

## Overview
PlacementHub is a comprehensive web-based placement portal application built for institutes to manage campus recruitment activities. It facilitates interaction between three main roles: Admin (Institute Placement Cell), Companies, and Students.
## Features
### Admin Features
- Dashboard with statistics (students, companies, drives, applications)
- Approve/reject company registrations
- Approve/reject placement drives
- Manage and blacklist students and companies
- Search functionality for students and companies
- View all applications and placement records
### Company Features
- Company registration and profile management
- Create, edit, and delete placement drives (post-approval)
- View student applications for their drives
- Shortlist/select/reject applicants
- Update application statuses

### Student Features
- Student self-registration and login
- View and apply for approved placement drives
- Track application status and history
- Update profile and upload resume
- Prevent duplicate applications

## Technology Stack
- **Backend**: Flask 3.0.0
- **Frontend**: Jinja2 templates, HTML5, CSS3, Bootstrap 5
- **Database**: SQLite3
- **Authentication**: Flask-Login
- **APIs**: RESTful JSON APIs using Flask-RESTful

## Installation
### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Instructions
1. Clone or extract the project to your local machine
2. Navigate to the project directory:
```bash
cd placement_portal
```
3. Create a virtual environment (recommended):
```bash
python -m venv venv
```
4. Activate the virtual environment:
- Windows:
  ```bash
  venv\Scripts\activate
  ```
- Linux/Mac:
  ```bash
  source venv/bin/activate
  ```
5. Install required dependencies:
```bash
pip install -r requirements.txt
```
6. Run the application:
```bash
python app.py
``
7. Open your browser and navigate to:
```
http://localhost:5000
```
## Default Admin Credentials
- **Email**: admin@placement.com
- **Password**: admin123

## Project Structure
```
placement_portal/
├── app.py                      # Main Flask application
├── models.py                   # Database models and initialization
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── placement.db               # SQLite database (auto-created)
├── static/
│   ├── css/
│   │   └── style.css          # Custom styling
│   ├── js/
│   │   └── charts.js          # JavaScript for charts
│   └── uploads/
│       └── resumes/           # Uploaded resume files
├── templates/
│   ├── base.html              # Base template
│   ├── auth/
│   │   ├── login.html         # Login page
│   │   ├── register_student.html
│   │   └── register_company.html
│   ├── admin/
│   │   ├── dashboard.html     # Admin dashboard
│   │   ├── companies.html     # Manage companies
│   │   ├── students.html      # Manage students
│   │   ├── drives.html        # Manage drives
│   │   └── applications.html  # View applications
│   ├── company/
│   │   ├── dashboard.html     # Company dashboard
│   │   ├── post_drive.html    # Create/edit drive
│   │   ├── applications.html  # View applications
│   │   └── profile.html       # Company profile
│   └── student/
│       ├── dashboard.html     # Student dashboard
│       ├── drives.html        # Browse drives
│       ├── applications.html  # Application history
│       └── profile.html       # Student profile
└── api/
    ├── __init__.py
    ├── students.py            # Student API endpoints
    ├── companies.py           # Company API endpoints
    └── applications.py        # Applications & Drives API
```
## Database Schema

### Tables
1. **admin** - Admin user details
2. **company** - Company profiles with approval status
3. **student** - Student profiles and academic details
4. **placement_drive** - Job postings by companies
5. **application** - Student applications to drives
6. **notification** - Notifications for students

### Key Relationships
- Companies → Placement Drives (One-to-Many)
- Students → Applications (One-to-Many)
- Placement Drives → Applications (One-to-Many)
- Applications → Students (Many-to-One)

## API Endpoints

### Students API
- `GET /api/students` - List all students
- `GET /api/students/<id>` - Get student details
- `POST /api/students` - Create student
- `PUT /api/students/<id>` - Update student
- `DELETE /api/students/<id>` - Delete student

### Companies API
- `GET /api/companies` - List all companies
- `GET /api/companies/<id>` - Get company details
- `POST /api/companies` - Create company
- `PUT /api/companies/<id>` - Update company
- `DELETE /api/companies/<id>` - Delete company

### Drives API
- `GET /api/drives` - List active drives
- `GET /api/drives/all` - List all drives
- `GET /api/drives/<id>` - Get drive details
- `PUT /api/drives/<id>` - Update drive status
- `DELETE /api/drives/<id>` - Delete drive

### Applications API
- `GET /api/applications` - List all applications
- `GET /api/applications/<id>` - Get application details
- `POST /api/applications` - Submit application
- `PUT /api/applications/<id>` - Update application status
- `DELETE /api/applications/<id>` - Delete application

## Usage Workflow

### For Students
1. Register using student registration form
2. Log in with credentials
3. Complete profile and upload resume
4. Browse active placement drives
5. Apply for drives with cover letter
6. Track application status

### For Companies
1. Register using company registration form
2. Wait for admin approval
3. Log in after approval
4. Complete company profile
5. Create placement drives
6. Wait for admin approval of drives
7. View and manage applications
8. Shortlist/select candidates

### For Admin
1. Log in with admin credentials
2. Approve/reject company registrations
3. Approve/reject placement drives
4. Monitor all activities
5. Search and manage users
6. Blacklist if necessary

## Security Features
- Password hashing using Werkzeug
- Role-based access control
- Login required decorators
- CSRF protection (Flask-WTF)
- Secure file uploads
- SQL injection prevention

## Additional Features
- Responsive UI with Bootstrap 5
- Charts for statistics visualization
- Flash messages for user feedback
- Search functionality
- Duplicate application prevention
- Notification system
- Resume file management

## Development Notes
- Database is created automatically on first run
- Admin user is seeded by default
- Debug mode is enabled in development
- Maximum resume upload size: 5MB
- Allowed resume formats: PDF, DOC, DOCX
## License
Educational project for campus placement management.

## Support
For issues or questions, please refer to the project documentation.


