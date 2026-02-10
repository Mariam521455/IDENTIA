from flask import Blueprint, render_template
from flask_login import login_required, current_user

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@main_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@main_bp.route('/students')
@login_required
def students_list():
    return render_template('students.html')

@main_bp.route('/attendance')
@login_required
def attendance_mgmt():
    return render_template('attendance.html')

@main_bp.route('/audit')
@login_required
def audit_view():
    # Only for SUPER_ADMIN or TECH_USER
    if current_user.role not in ['SUPER_ADMIN', 'TECH_USER']:
        return "Access Forbidden", 403
    return render_template('audit.html')
