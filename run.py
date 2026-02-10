from app import create_app, db, login
from app.domain.models.user import User, AuditLog
from app.domain.models.attendance import Student, Classroom, AttendanceSession, Attendance
import click

app = create_app()

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db, 
        'User': User, 
        'Student': Student, 
        'Attendance': Attendance,
        'AuditLog': AuditLog
    }

@app.cli.command("init-db")
def init_db():
    """Initialize the database with a default Super Admin."""
    db.create_all()
    
    # Check if super admin exists
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@identia.local',
            full_name='Super Administrateur',
            role='SUPER_ADMIN'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        click.echo("Database initialized with Super Admin (admin/admin123).")
    else:
        click.echo("Database already initialized.")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
