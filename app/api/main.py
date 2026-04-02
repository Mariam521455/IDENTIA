from flask import Blueprint, render_template, current_app
from flask_login import login_required, current_user
from app.domain.services.attendance_service import AttendanceService
from app.domain.models.schedule import AcademicClass
from app.domain.models.user import AuditLog

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/portal')
def portal():
    # Pass classes for enrollment if needed, though recognition.py handles /enroll
    return render_template('portal.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    stats = AttendanceService.get_dashboard_stats()
    recent_logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).limit(10).all()
    return render_template('dashboard.html', stats=stats, recent_logs=recent_logs)

@main_bp.route('/students')
@login_required
def students_list():
    students = Student.query.all()
    classes = AcademicClass.query.all()
    return render_template('students.html', students=students, classes=classes)

@main_bp.route('/classes')
@login_required
def classes_list():
    classes = AcademicClass.query.all()
    return render_template('classes.html', classes=classes)

@main_bp.route('/schedules')
@login_required
def schedules_list():
    schedules = Schedule.query.all()
    return render_template('schedules.html', schedules=schedules)

@main_bp.route('/audit')
@login_required
def audit_view():
    if current_user.role not in ['SUPER_ADMIN', 'TECH_USER']:
        return "Access Forbidden", 403
    logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).all()
    return render_template('audit.html', logs=logs)
