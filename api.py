from flask import Blueprint, jsonify

from models import Application, Company, PlacementDrive, Student

api_bp = Blueprint('api', __name__)


@api_bp.route('/students', methods=['GET'])
def students():
    data = [
        {
            'id': student.id,
            'name': student.name,
            'email': student.email,
            'department': student.department,
            'year_of_study': student.year_of_study,
        }
        for student in Student.query.all()
    ]
    return jsonify(data)


@api_bp.route('/companies', methods=['GET'])
def companies():
    data = [
        {
            'id': company.id,
            'company_name': company.company_name,
            'email': company.email,
            'industry': company.industry,
            'approval_status': company.approval_status,
        }
        for company in Company.query.all()
    ]
    return jsonify(data)


@api_bp.route('/drives', methods=['GET'])
def drives():
    data = [
        {
            'id': drive.id,
            'company_id': drive.company_id,
            'job_title': drive.job_title,
            'status': drive.status,
            'application_deadline': drive.application_deadline.isoformat(),
        }
        for drive in PlacementDrive.query.all()
    ]
    return jsonify(data)


@api_bp.route('/applications', methods=['GET'])
def applications():
    data = [
        {
            'id': application.id,
            'student_id': application.student_id,
            'drive_id': application.drive_id,
            'status': application.status,
        }
        for application in Application.query.all()
    ]
    return jsonify(data)
