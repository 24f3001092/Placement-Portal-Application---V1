# App Dev Project Report

## 1. Student Details

**Name:** Saurav Kumar  
**Roll Number:** 24f3001092  
**Email:** 24f3001092@ds.study.iitm.ac.in  
**About Me:** I am a student pursuing an online degree with a strong interest in full-stack web development. This project gave me hands-on experience in designing and implementing a real-world multi-role web application using Flask, Python, SQLAlchemy, server-rendered templates, and role-based workflows.

## 2. Project Details

**Project Title:** Placement Portal

**Problem Statement:**  
To design and build a web-based placement management system that connects students, companies, and an administrator in a single platform. The system should streamline campus recruitment activities such as registration, company approval, placement drive creation, student applications, profile management, and application status tracking.

**Approach:**  
This project is built using Flask with Blueprint-based route separation for authentication, admin, company, student, and API functionality. The application uses SQLAlchemy models for database design and CRUD operations, Flask session management for role-based access control, and Flask-Bcrypt for secure password hashing. A default administrator account is automatically created on first run if no admin exists (`admin@placement.com` / `admin123`). The user interface is implemented using Jinja2 templates, Bootstrap 5, Bootstrap Icons, and custom CSS.

## 3. AI/LLM Declaration

Based on a review of the current repository contents (`placement_portal/app.py`, `placement_portal/router.py`, `placement_portal/models.py`, `placement_portal/api.py`, templates, static assets, and `requirements.txt`), the application itself does not implement any AI or LLM functionality. No AI-specific libraries such as OpenAI, LangChain, Hugging Face, TensorFlow, PyTorch, Anthropic, Cohere, or similar packages are imported in the project source files or listed in the dependency file.

All major features in this codebase - authentication, role management, admin approvals, placement drive management, student applications, resume handling, and JSON API responses - are implemented using Flask, SQLAlchemy, Flask-Bcrypt, Jinja2, Bootstrap, and standard Python utilities.

## 4. Technologies and Frameworks Used

| Technology / Library | Source File(s) | Purpose |
| --- | --- | --- |
| Flask | `placement_portal/app.py`, `placement_portal/router.py`, `placement_portal/api.py` | Core web framework for routing, sessions, Blueprint registration, request handling, redirects, flash messages, and JSON responses |
| Flask-SQLAlchemy | `placement_portal/models.py`, `placement_portal/app.py` | ORM layer for defining models, relationships, queries, and database initialization |
| Flask-Bcrypt | `placement_portal/models.py` | Password hashing and verification through `set_password()` and `check_password()` methods |
| SQLite | `placement_portal/app.py`, `instance/placement_portal.db` | File-based relational database used to store admins, companies, students, drives, and applications |
| Jinja2 | `placement_portal/templates/`, `placement_portal/router.py` | Server-side HTML rendering for all role-based dashboards, forms, and listings |
| Bootstrap 5 | `placement_portal/templates/base.html` | Responsive layout, cards, forms, tables, alerts, navbar, and modal UI components |
| Bootstrap Icons | `placement_portal/templates/base.html` | Iconography used across dashboards and navigation |
| Custom CSS | `placement_portal/static/css/style.css` | Application-specific styling for cards, navbar layout, drive cards, forms, and status display |
| Vanilla JavaScript | `placement_portal/static/js/*.js` | Frontend helper scripts for simple validation, chart rendering hooks, and notification behavior |
| Werkzeug `secure_filename` | `placement_portal/router.py` | Safe file naming for uploaded resumes |
| Flask Session | `placement_portal/router.py` | Maintains logged-in user state with `user_id`, `role`, and `name` in session storage |

## 5. Database Schema

The database schema is defined in `placement_portal/models.py` using SQLAlchemy ORM models.

**Relationships**

- `Company` -> `PlacementDrive` (one-to-many)
- `Student` -> `Application` (one-to-many)
- `PlacementDrive` -> `Application` (one-to-many)
- Parent-child relationships use `cascade='all, delete-orphan'` so dependent records are removed when the parent entity is deleted

### Table 1: `admin`

| Field | Type | Constraints / Description |
| --- | --- | --- |
| `id` | Integer | Primary key |
| `username` | String(50) | Unique, not null |
| `email` | String(120) | Unique, not null |
| `password_hash` | String(128) | Not null |
| `created_at` | DateTime | Default: `datetime.utcnow` |

This table stores administrator credentials. On first application startup, the app auto-seeds a default admin account if the table is empty.

### Table 2: `company`

| Field | Type | Constraints / Description |
| --- | --- | --- |
| `id` | Integer | Primary key |
| `company_name` | String(120) | Not null |
| `email` | String(120) | Unique, not null |
| `password_hash` | String(128) | Not null |
| `hr_contact` | String(20) | Nullable |
| `website` | String(200) | Nullable |
| `industry` | String(100) | Nullable |
| `description` | Text | Nullable |
| `approval_status` | String(20) | Default: `Pending` |
| `is_blacklisted` | Boolean | Default: `False` |
| `created_at` | DateTime | Default: `datetime.utcnow` |

`approval_status` is used for the company approval workflow with values such as `Pending`, `Approved`, and `Rejected`. A blacklisted company cannot access company routes even if previously approved.

### Table 3: `student`

| Field | Type | Constraints / Description |
| --- | --- | --- |
| `id` | Integer | Primary key |
| `name` | String(100) | Not null |
| `email` | String(120) | Unique, not null |
| `password_hash` | String(128) | Not null |
| `phone` | String(20) | Nullable |
| `department` | String(100) | Nullable |
| `year_of_study` | String(20) | Nullable |
| `cgpa` | Float | Nullable |
| `skills` | Text | Nullable |
| `resume_filename` | String(200) | Nullable |
| `is_blacklisted` | Boolean | Default: `False` |
| `is_active` | Boolean | Default: `True` |
| `created_at` | DateTime | Default: `datetime.utcnow` |

This table stores the student profile and academic details. `resume_filename` stores the saved uploaded resume name, typically in the format `email_originalfilename`. When a student is blacklisted by the admin, the account is also marked inactive.

### Table 4: `placement_drive`

| Field | Type | Constraints / Description |
| --- | --- | --- |
| `id` | Integer | Primary key |
| `company_id` | Integer | Foreign key -> `company.id`, not null |
| `job_title` | String(150) | Not null |
| `job_description` | Text | Not null |
| `eligibility_criteria` | Text | Nullable |
| `required_skills` | String(300) | Nullable |
| `salary_range` | String(100) | Nullable |
| `location` | String(100) | Nullable |
| `application_deadline` | Date | Not null |
| `status` | String(20) | Default: `Pending` |
| `created_at` | DateTime | Default: `datetime.utcnow` |

Placement drives are created by companies and reviewed by the admin. Typical workflow states are `Pending`, `Approved`, `Closed`, and `Rejected`. When a company edits an existing drive, the route logic resets the drive status back to `Pending` for re-approval.

### Table 5: `application`

| Field | Type | Constraints / Description |
| --- | --- | --- |
| `id` | Integer | Primary key |
| `student_id` | Integer | Foreign key -> `student.id`, not null |
| `drive_id` | Integer | Foreign key -> `placement_drive.id`, not null |
| `application_date` | DateTime | Default: `datetime.utcnow` |
| `status` | String(20) | Default: `Applied` |
| `cover_note` | Text | Nullable |

Additional database constraint:

- `UNIQUE(student_id, drive_id)` prevents a student from applying to the same placement drive more than once

Application status values used in the project are `Applied`, `Shortlisted`, `Selected`, and `Rejected`.

## 6. API Resource Endpoints

The project includes a dedicated API Blueprint in `placement_portal/api.py`, registered under the `/api` URL prefix in `placement_portal/app.py`. All API routes are currently read-only `GET` endpoints returning JSON responses through `jsonify()`.

| Endpoint | Method | Data Returned |
| --- | --- | --- |
| `/api/students` | `GET` | `id`, `name`, `email`, `department`, `year_of_study` for all students |
| `/api/companies` | `GET` | `id`, `company_name`, `email`, `industry`, `approval_status` for all companies |
| `/api/drives` | `GET` | `id`, `company_id`, `job_title`, `status`, `application_deadline` for all placement drives |
| `/api/applications` | `GET` | `id`, `student_id`, `drive_id`, `status` for all applications |

**Note:** No separate `api.yaml`, `openapi.yaml`, or similar API definition file is present in the current project folder snapshot.

## 7. Architecture and Features

### Project Structure

- `placement_portal/app.py` - main Flask application entry point; configures secret key, SQLite database URI, upload folder, 5 MB upload limit, registers Blueprints, defines the root redirect route, creates database tables, and seeds the default admin
- `placement_portal/router.py` - central routing module containing Blueprint definitions, access-control decorators, authentication routes, and all admin, company, and student route handlers
- `placement_portal/models.py` - SQLAlchemy models for `Admin`, `Company`, `Student`, `PlacementDrive`, and `Application`, along with password helper methods
- `placement_portal/api.py` - JSON API Blueprint exposing read-only resource endpoints
- `placement_portal/templates/` - Jinja2 templates organized into `auth/`, `admin/`, `company/`, and `student/` directories
- `placement_portal/static/css/style.css` - custom styling for the portal UI
- `placement_portal/static/js/` - JavaScript helper scripts for frontend enhancements
- `placement_portal/static/uploads/resumes/` - uploaded student resumes stored inside the static directory for viewing/download
- `instance/placement_portal.db` - SQLite database file generated by the application in the Flask instance folder
- `README.md` and `requirements.txt` - project documentation and dependency list

### Core Features

**Authentication and Access Control**

- Multi-role login for Admin, Company, and Student users
- Session-based access control using custom decorators such as `admin_required`, `company_required`, and `student_required`
- Company login is blocked if the company is pending approval, rejected, or blacklisted
- Student login is blocked if the account is deactivated or blacklisted
- Logout clears the active session

**Admin Module**

- Dashboard with counts of students, companies, drives, and applications
- Quick visibility into pending company approvals and pending drive approvals
- Company management including approve, reject, blacklist/unblacklist, edit, and delete
- Student management including search, blacklist/unblacklist, edit, and delete
- Placement drive review including approve, reject, and delete
- Global applications view ordered by recent activity

**Company Module**

- Company self-registration with details such as HR contact, website, industry, and description
- Dashboard listing company drives and applicant counts
- Create new placement drives with role details, skills, salary range, location, and application deadline
- Edit existing drives, with automatic re-submission for admin approval
- Close or delete posted drives
- View all applications received for a drive
- Update student application status to `Shortlisted`, `Selected`, or `Rejected`
- Maintain a company profile page

**Student Module**

- Student self-registration with academic details, skills, and optional resume upload
- Browse only approved drives whose application deadline has not passed
- Search drives by job title or required skills
- Apply to drives with an optional cover note
- Duplicate applications are prevented both in route logic and at the database level
- Track application history and status updates
- Update personal profile details and replace the uploaded resume

**Frontend and UI**

- Responsive UI built with Bootstrap cards, tables, alerts, forms, navbar, and modal dialogs
- Common layout in `base.html` with role-aware navigation links
- Resume viewing links available to both students and companies
- Flash messages used throughout the application for action feedback

## 8. Video

**Project Demonstration Video Link:**  
Add your Google Drive or YouTube project demo link here before final submission.

---

**Summary:**  
The Placement Portal is a multi-user campus recruitment system implemented with Flask, SQLAlchemy, SQLite, and Jinja2. It provides a complete workflow for company onboarding, admin approval, placement drive publishing, student applications, and application status management, all within a structured role-based web interface.
