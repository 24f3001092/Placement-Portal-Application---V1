from flask import Flask
from models import db
from router import auth_bp, admin_bp, company_bp, student_bp
from api import api_bp
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'placement-portal-secret-key-2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///placement_portal.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'static', 'uploads', 'resumes')
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB

db.init_app(app) 

app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(company_bp, url_prefix='/company')
app.register_blueprint(student_bp, url_prefix='/student')
app.register_blueprint(api_bp, url_prefix='/api')

from flask import redirect, url_for, session

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    role = session.get('role')
    if role == 'admin':
        return redirect(url_for('admin.dashboard'))
    elif role == 'company':
        return redirect(url_for('company.dashboard'))
    elif role == 'student':
        return redirect(url_for('student.dashboard'))
    return redirect(url_for('auth.login'))

with app.app_context():
    db.create_all()
    from models import Admin, bcrypt
    if not Admin.query.first():
        admin = Admin(username='admin', email='admin@placement.com')
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("Admin created: admin@placement.com / admin123")

if __name__ == '__main__':
    app.run(debug=True  )

