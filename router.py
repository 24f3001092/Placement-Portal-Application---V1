from datetime import date, datetime
from functools import wraps
import os

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from models import Application, Admin, Company, PlacementDrive, Student, db


auth_bp = Blueprint('auth', __name__)
admin_bp = Blueprint('admin', __name__)
company_bp = Blueprint('company', __name__)
student_bp = Blueprint('student', __name__)


def login_required(role=None):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if 'user_id' not in session:
                flash('Please log in to access this page.', 'warning')
                return redirect(url_for('auth.login'))
            if role and session.get('role') != role:
                flash('Unauthorized access.', 'danger')
                return redirect(url_for('auth.login'))
            return f(*args, **kwargs)

        return decorated

    return decorator


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'admin':
            flash('Admin access required.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)

    return decorated


def company_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'company':
            flash('Company access required.', 'danger')
            return redirect(url_for('auth.login'))
        company = Company.query.get(session['user_id'])
        if not company or company.approval_status != 'Approved' or company.is_blacklisted:
            flash('Access denied.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)

    return decorated


def student_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'student':
            flash('Student access required.', 'danger')
            return redirect(url_for('auth.login'))
        student = Student.query.get(session['user_id'])
        if not student or student.is_blacklisted or not student.is_active:
            flash('Your account is deactivated.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)

    return decorated


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        role = session.get('role')
        user_id = session.get('user_id')

        if role == 'admin':
            if Admin.query.get(user_id):
                return redirect(url_for('admin.dashboard'))
        elif role == 'company':
            company = Company.query.get(user_id)
            if company and company.approval_status == 'Approved' and not company.is_blacklisted:
                return redirect(url_for('company.dashboard'))
        elif role == 'student':
            student = Student.query.get(user_id)
            if student and student.is_active and not student.is_blacklisted:
                return redirect(url_for('student.dashboard'))

        session.clear()
        flash('Your session expired. Please log in again.', 'info')
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        role = request.form.get('role', '')

        if role == 'admin':
            user = Admin.query.filter_by(email=email).first()
            if user and user.check_password(password):
                session['user_id'] = user.id
                session['role'] = 'admin'
                session['name'] = user.username
                return redirect(url_for('admin.dashboard'))
        elif role == 'company':
            user = Company.query.filter_by(email=email).first()
            if user and user.check_password(password):
                if user.is_blacklisted:
                    flash('Your account has been blacklisted. Contact admin.', 'danger')
                    return redirect(url_for('auth.login'))
                if user.approval_status == 'Pending':
                    flash('Your registration is pending admin approval.', 'warning')
                    return redirect(url_for('auth.login'))
                if user.approval_status == 'Rejected':
                    flash('Your registration was rejected by admin.', 'danger')
                    return redirect(url_for('auth.login'))
                session['user_id'] = user.id
                session['role'] = 'company'
                session['name'] = user.company_name
                return redirect(url_for('company.dashboard'))
        elif role == 'student':
            user = Student.query.filter_by(email=email).first()
            if user and user.check_password(password):
                if user.is_blacklisted or not user.is_active:
                    flash('Your account has been deactivated. Contact admin.', 'danger')
                    return redirect(url_for('auth.login'))
                session['user_id'] = user.id
                session['role'] = 'student'
                session['name'] = user.name
                return redirect(url_for('student.dashboard'))

        flash('Invalid credentials. Please try again.', 'danger')
    return render_template('auth/login.html')


@auth_bp.route('/register/company', methods=['GET', 'POST'])
def register_company():
    if request.method == 'POST':
        company_name = request.form.get('company_name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')
        hr_contact = request.form.get('hr_contact', '').strip()
        website = request.form.get('website', '').strip()
        industry = request.form.get('industry', '').strip()
        description = request.form.get('description', '').strip()

        if not company_name or not email or not password:
            flash('Company name, email and password are required.', 'danger')
            return render_template('auth/register_company.html')
        if password != confirm:
            flash('Passwords do not match.', 'danger')
            return render_template('auth/register_company.html')
        if Company.query.filter_by(email=email).first():
            flash('Email already registered.', 'danger')
            return render_template('auth/register_company.html')

        company = Company(
            company_name=company_name,
            email=email,
            hr_contact=hr_contact,
            website=website,
            industry=industry,
            description=description,
        )
        company.set_password(password)
        db.session.add(company)
        db.session.commit()
        flash('Registration submitted! Awaiting admin approval.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register_company.html')


@auth_bp.route('/register/student', methods=['GET', 'POST'])
def register_student():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')
        phone = request.form.get('phone', '').strip()
        department = request.form.get('department', '').strip()
        year_of_study = request.form.get('year_of_study', '').strip()
        cgpa_str = request.form.get('cgpa', '').strip()
        skills = request.form.get('skills', '').strip()

        if not name or not email or not password:
            flash('Name, email and password are required.', 'danger')
            return render_template('auth/register_student.html')
        if password != confirm:
            flash('Passwords do not match.', 'danger')
            return render_template('auth/register_student.html')
        if Student.query.filter_by(email=email).first():
            flash('Email already registered.', 'danger')
            return render_template('auth/register_student.html')

        cgpa = float(cgpa_str) if cgpa_str else None
        resume_filename = None

        if 'resume' in request.files:
            resume = request.files['resume']
            if resume and resume.filename:
                from werkzeug.utils import secure_filename

                filename = secure_filename(f"{email}_{resume.filename}")
                upload_folder = os.path.join(
                    os.path.dirname(os.path.abspath(__file__)),
                    'static',
                    'uploads',
                    'resumes',
                )
                os.makedirs(upload_folder, exist_ok=True)
                resume.save(os.path.join(upload_folder, filename))
                resume_filename = filename

        student = Student(
            name=name,
            email=email,
            phone=phone,
            department=department,
            year_of_study=year_of_study,
            cgpa=cgpa,
            skills=skills,
            resume_filename=resume_filename,
        )
        student.set_password(password)
        db.session.add(student)
        db.session.commit()
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register_student.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))


@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    total_students = Student.query.count()
    total_companies = Company.query.count()
    total_drives = PlacementDrive.query.count()
    total_applications = Application.query.count()
    pending_companies = Company.query.filter_by(approval_status='Pending').count()
    pending_drives = PlacementDrive.query.filter_by(status='Pending').count()
    recent_applications = Application.query.order_by(Application.application_date.desc()).limit(5).all()
    return render_template(
        'admin/dashboard.html',
        total_students=total_students,
        total_companies=total_companies,
        total_drives=total_drives,
        total_applications=total_applications,
        pending_companies=pending_companies,
        pending_drives=pending_drives,
        recent_applications=recent_applications,
    )


@admin_bp.route('/companies')
@admin_required
def companies():
    search = request.args.get('search', '').strip()
    query = Company.query
    if search:
        query = query.filter((Company.company_name.ilike(f'%{search}%')) | (Company.id.like(f'%{search}%')))
    companies = query.order_by(Company.created_at.desc()).all()
    return render_template('admin/companies.html', companies=companies, search=search)


@admin_bp.route('/company/<int:company_id>/approve', methods=['POST'])
@admin_required
def approve_company(company_id):
    company = Company.query.get_or_404(company_id)
    company.approval_status = 'Approved'
    db.session.commit()
    flash(f'{company.company_name} approved successfully.', 'success')
    return redirect(url_for('admin.companies'))


@admin_bp.route('/company/<int:company_id>/reject', methods=['POST'])
@admin_required
def reject_company(company_id):
    company = Company.query.get_or_404(company_id)
    company.approval_status = 'Rejected'
    db.session.commit()
    flash(f'{company.company_name} rejected.', 'warning')
    return redirect(url_for('admin.companies'))


@admin_bp.route('/company/<int:company_id>/blacklist', methods=['POST'])
@admin_required
def blacklist_company(company_id):
    company = Company.query.get_or_404(company_id)
    company.is_blacklisted = not company.is_blacklisted
    status = 'blacklisted' if company.is_blacklisted else 'unblacklisted'
    db.session.commit()
    flash(f'{company.company_name} {status}.', 'info')
    return redirect(url_for('admin.companies'))


@admin_bp.route('/company/<int:company_id>/delete', methods=['POST'])
@admin_required
def delete_company(company_id):
    company = Company.query.get_or_404(company_id)
    db.session.delete(company)
    db.session.commit()
    flash('Company deleted.', 'success')
    return redirect(url_for('admin.companies'))


@admin_bp.route('/company/<int:company_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_company(company_id):
    company = Company.query.get_or_404(company_id)
    if request.method == 'POST':
        company_name = request.form.get('company_name', '').strip()
        email = request.form.get('email', '').strip()
        if not company_name or not email:
            flash('Company name and email are required.', 'danger')
            return render_template('admin/edit_company.html', company=company)

        existing = Company.query.filter(Company.email == email, Company.id != company.id).first()
        if existing:
            flash('Email already exists for another company.', 'danger')
            return render_template('admin/edit_company.html', company=company)

        company.company_name = company_name
        company.email = email
        company.hr_contact = request.form.get('hr_contact', '').strip()
        company.website = request.form.get('website', '').strip()
        company.industry = request.form.get('industry', '').strip()
        company.description = request.form.get('description', '').strip()
        db.session.commit()
        flash('Company updated successfully.', 'success')
        return redirect(url_for('admin.companies'))
    return render_template('admin/edit_company.html', company=company)


@admin_bp.route('/students')
@admin_required
def students():
    search = request.args.get('search', '').strip()
    query = Student.query
    if search:
        query = query.filter(
            (Student.name.ilike(f'%{search}%'))
            | (Student.email.ilike(f'%{search}%'))
            | (Student.phone.ilike(f'%{search}%'))
            | (Student.id.like(f'%{search}%'))
        )
    students = query.order_by(Student.created_at.desc()).all()
    return render_template('admin/students.html', students=students, search=search)


@admin_bp.route('/student/<int:student_id>/blacklist', methods=['POST'])
@admin_required
def blacklist_student(student_id):
    student = Student.query.get_or_404(student_id)
    student.is_blacklisted = not student.is_blacklisted
    student.is_active = not student.is_blacklisted
    status = 'blacklisted' if student.is_blacklisted else 'unblacklisted'
    db.session.commit()
    flash(f'{student.name} {status}.', 'info')
    return redirect(url_for('admin.students'))


@admin_bp.route('/student/<int:student_id>/delete', methods=['POST'])
@admin_required
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    flash('Student deleted.', 'success')
    return redirect(url_for('admin.students'))


@admin_bp.route('/student/<int:student_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_student(student_id):
    student = Student.query.get_or_404(student_id)
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        if not name or not email:
            flash('Student name and email are required.', 'danger')
            return render_template('admin/edit_student.html', student=student)

        existing = Student.query.filter(Student.email == email, Student.id != student.id).first()
        if existing:
            flash('Email already exists for another student.', 'danger')
            return render_template('admin/edit_student.html', student=student)

        student.name = name
        student.email = email
        student.phone = request.form.get('phone', '').strip()
        student.department = request.form.get('department', '').strip()
        student.year_of_study = request.form.get('year_of_study', '').strip()
        cgpa_str = request.form.get('cgpa', '').strip()
        student.cgpa = float(cgpa_str) if cgpa_str else None
        student.skills = request.form.get('skills', '').strip()
        student.is_active = request.form.get('is_active') == 'on'
        if not student.is_active:
            student.is_blacklisted = True
        db.session.commit()
        flash('Student updated successfully.', 'success')
        return redirect(url_for('admin.students'))
    return render_template('admin/edit_student.html', student=student)


@admin_bp.route('/drives')
@admin_required
def drives():
    drives = PlacementDrive.query.order_by(PlacementDrive.created_at.desc()).all()
    return render_template('admin/drives.html', drives=drives)


@admin_bp.route('/drive/<int:drive_id>/approve', methods=['POST'])
@admin_required
def approve_drive(drive_id):
    drive = PlacementDrive.query.get_or_404(drive_id)
    drive.status = 'Approved'
    db.session.commit()
    flash('Placement drive approved.', 'success')
    return redirect(url_for('admin.drives'))


@admin_bp.route('/drive/<int:drive_id>/reject', methods=['POST'])
@admin_required
def reject_drive(drive_id):
    drive = PlacementDrive.query.get_or_404(drive_id)
    drive.status = 'Rejected'
    db.session.commit()
    flash('Placement drive rejected.', 'warning')
    return redirect(url_for('admin.drives'))


@admin_bp.route('/drive/<int:drive_id>/delete', methods=['POST'])
@admin_required
def delete_drive(drive_id):
    drive = PlacementDrive.query.get_or_404(drive_id)
    db.session.delete(drive)
    db.session.commit()
    flash('Drive deleted.', 'success')
    return redirect(url_for('admin.drives'))


@admin_bp.route('/applications')
@admin_required
def applications():
    applications = Application.query.order_by(Application.application_date.desc()).all()
    return render_template('admin/applications.html', applications=applications)


@company_bp.route('/dashboard')
@company_required
def dashboard():
    company = Company.query.get(session['user_id'])
    drives = PlacementDrive.query.filter_by(company_id=company.id).order_by(PlacementDrive.created_at.desc()).all()
    drive_stats = []
    for drive in drives:
        count = Application.query.filter_by(drive_id=drive.id).count()
        drive_stats.append({'drive': drive, 'applicant_count': count})
    total_applicants = Application.query.join(PlacementDrive).filter(PlacementDrive.company_id == company.id).count()
    return render_template(
        'company/dashboard.html',
        company=company,
        drive_stats=drive_stats,
        total_applicants=total_applicants,
    )


@company_bp.route('/drives/create', methods=['GET', 'POST'])
@company_required
def create_drive():
    company = Company.query.get(session['user_id'])
    if request.method == 'POST':
        job_title = request.form.get('job_title', '').strip()
        job_description = request.form.get('job_description', '').strip()
        eligibility_criteria = request.form.get('eligibility_criteria', '').strip()
        required_skills = request.form.get('required_skills', '').strip()
        salary_range = request.form.get('salary_range', '').strip()
        location = request.form.get('location', '').strip()
        deadline_str = request.form.get('application_deadline', '')

        if not job_title or not job_description or not deadline_str:
            flash('Job title, description and deadline are required.', 'danger')
            return render_template('company/create_drive.html')

        deadline = datetime.strptime(deadline_str, '%Y-%m-%d').date()
        drive = PlacementDrive(
            company_id=company.id,
            job_title=job_title,
            job_description=job_description,
            eligibility_criteria=eligibility_criteria,
            required_skills=required_skills,
            salary_range=salary_range,
            location=location,
            application_deadline=deadline,
        )
        db.session.add(drive)
        db.session.commit()
        flash('Placement drive submitted for admin approval.', 'success')
        return redirect(url_for('company.dashboard'))
    return render_template('company/create_drive.html')


@company_bp.route('/drives/<int:drive_id>/edit', methods=['GET', 'POST'])
@company_required
def edit_drive(drive_id):
    company = Company.query.get(session['user_id'])
    drive = PlacementDrive.query.filter_by(id=drive_id, company_id=company.id).first_or_404()
    if request.method == 'POST':
        drive.job_title = request.form.get('job_title', '').strip()
        drive.job_description = request.form.get('job_description', '').strip()
        drive.eligibility_criteria = request.form.get('eligibility_criteria', '').strip()
        drive.required_skills = request.form.get('required_skills', '').strip()
        drive.salary_range = request.form.get('salary_range', '').strip()
        drive.location = request.form.get('location', '').strip()
        deadline_str = request.form.get('application_deadline', '')
        if deadline_str:
            drive.application_deadline = datetime.strptime(deadline_str, '%Y-%m-%d').date()
        drive.status = 'Pending'
        db.session.commit()
        flash('Drive updated and resubmitted for approval.', 'success')
        return redirect(url_for('company.dashboard'))
    return render_template('company/edit_drive.html', drive=drive)


@company_bp.route('/drives/<int:drive_id>/close', methods=['POST'])
@company_required
def close_drive(drive_id):
    company = Company.query.get(session['user_id'])
    drive = PlacementDrive.query.filter_by(id=drive_id, company_id=company.id).first_or_404()
    drive.status = 'Closed'
    db.session.commit()
    flash('Drive closed.', 'info')
    return redirect(url_for('company.dashboard'))


@company_bp.route('/drives/<int:drive_id>/delete', methods=['POST'])
@company_required
def delete_drive(drive_id):
    company = Company.query.get(session['user_id'])
    drive = PlacementDrive.query.filter_by(id=drive_id, company_id=company.id).first_or_404()
    db.session.delete(drive)
    db.session.commit()
    flash('Drive deleted.', 'success')
    return redirect(url_for('company.dashboard'))


@company_bp.route('/drives/<int:drive_id>/applications')
@company_required
def drive_applications(drive_id):
    company = Company.query.get(session['user_id'])
    drive = PlacementDrive.query.filter_by(id=drive_id, company_id=company.id).first_or_404()
    applications = Application.query.filter_by(drive_id=drive.id).all()
    return render_template('company/applications.html', drive=drive, applications=applications)


@company_bp.route('/application/<int:app_id>/status', methods=['POST'])
@company_required
def update_status(app_id):
    company = Company.query.get(session['user_id'])
    application = Application.query.get_or_404(app_id)
    drive = PlacementDrive.query.filter_by(id=application.drive_id, company_id=company.id).first_or_404()
    new_status = request.form.get('status', '')
    if new_status in ['Shortlisted', 'Selected', 'Rejected']:
        application.status = new_status
        db.session.commit()
        flash(f'Application status updated to {new_status}.', 'success')
    return redirect(url_for('company.drive_applications', drive_id=drive.id))


@company_bp.route('/profile', methods=['GET', 'POST'])
@company_required
def profile():
    company = Company.query.get(session['user_id'])
    if request.method == 'POST':
        company.hr_contact = request.form.get('hr_contact', '').strip()
        company.website = request.form.get('website', '').strip()
        company.industry = request.form.get('industry', '').strip()
        company.description = request.form.get('description', '').strip()
        db.session.commit()
        session['name'] = company.company_name
        flash('Profile updated.', 'success')
        return redirect(url_for('company.profile'))
    return render_template('company/profile.html', company=company)


@student_bp.route('/dashboard')
@student_required
def dashboard():
    student = Student.query.get(session['user_id'])
    approved_drives = (
        PlacementDrive.query.filter_by(status='Approved')
        .filter(PlacementDrive.application_deadline >= date.today())
        .order_by(PlacementDrive.created_at.desc())
        .all()
    )
    applied_ids = {a.drive_id for a in Application.query.filter_by(student_id=student.id).all()}
    my_applications = (
        Application.query.filter_by(student_id=student.id)
        .order_by(Application.application_date.desc())
        .all()
    )
    return render_template(
        'student/dashboard.html',
        student=student,
        approved_drives=approved_drives,
        applied_ids=applied_ids,
        my_applications=my_applications,
    )


@student_bp.route('/drives')
@student_required
def drives():
    search = request.args.get('search', '').strip()
    query = PlacementDrive.query.filter_by(status='Approved').filter(
        PlacementDrive.application_deadline >= date.today()
    )
    if search:
        query = query.filter(
            (PlacementDrive.job_title.ilike(f'%{search}%'))
            | (PlacementDrive.required_skills.ilike(f'%{search}%'))
        )
    drives = query.order_by(PlacementDrive.created_at.desc()).all()
    student = Student.query.get(session['user_id'])
    applied_ids = {a.drive_id for a in Application.query.filter_by(student_id=student.id).all()}
    return render_template('student/drives.html', drives=drives, applied_ids=applied_ids, search=search)


@student_bp.route('/drive/<int:drive_id>/apply', methods=['POST'])
@student_required
def apply(drive_id):
    student = Student.query.get(session['user_id'])
    drive = PlacementDrive.query.filter_by(id=drive_id, status='Approved').first_or_404()
    if drive.application_deadline < date.today():
        flash('This drive has closed.', 'warning')
        return redirect(url_for('student.drives'))

    existing = Application.query.filter_by(student_id=student.id, drive_id=drive_id).first()
    if existing:
        flash('You have already applied for this drive.', 'warning')
        return redirect(url_for('student.drives'))

    cover_note = request.form.get('cover_note', '').strip()
    application = Application(student_id=student.id, drive_id=drive_id, cover_note=cover_note)
    db.session.add(application)
    db.session.commit()
    flash(f'Successfully applied for {drive.job_title}!', 'success')
    return redirect(url_for('student.my_applications'))


@student_bp.route('/applications')
@student_required
def my_applications():
    student = Student.query.get(session['user_id'])
    applications = (
        Application.query.filter_by(student_id=student.id)
        .order_by(Application.application_date.desc())
        .all()
    )
    return render_template('student/applications.html', student=student, applications=applications)


@student_bp.route('/profile', methods=['GET', 'POST'])
@student_required
def profile():
    student = Student.query.get(session['user_id'])
    if request.method == 'POST':
        student.name = request.form.get('name', student.name).strip()
        student.phone = request.form.get('phone', '').strip()
        student.department = request.form.get('department', '').strip()
        student.year_of_study = request.form.get('year_of_study', '').strip()
        cgpa_str = request.form.get('cgpa', '').strip()
        student.cgpa = float(cgpa_str) if cgpa_str else student.cgpa
        student.skills = request.form.get('skills', '').strip()

        if 'resume' in request.files:
            resume = request.files['resume']
            if resume and resume.filename:
                from werkzeug.utils import secure_filename

                filename = secure_filename(f"{student.email}_{resume.filename}")
                upload_folder = os.path.join(
                    os.path.dirname(os.path.abspath(__file__)),
                    'static',
                    'uploads',
                    'resumes',
                )
                os.makedirs(upload_folder, exist_ok=True)
                resume.save(os.path.join(upload_folder, filename))
                student.resume_filename = filename

        db.session.commit()
        session['name'] = student.name
        flash('Profile updated successfully.', 'success')
        return redirect(url_for('student.profile'))
    return render_template('student/profile.html', student=student)