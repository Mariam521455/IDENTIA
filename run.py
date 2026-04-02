from app import create_app, db, login
from app.domain.models.user import User, AuditLog
from app.domain.models.attendance import Student, Classroom, AttendanceSession, Attendance, FacialEncoding
from app.domain.models.schedule import AcademicClass, Schedule
from datetime import time
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
        'AuditLog': AuditLog,
        'AcademicClass': AcademicClass,
        'Schedule': Schedule,
        'FacialEncoding': FacialEncoding
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
        
        # Add Sample Classes (L1, L2, L3, Master1, Master2)
        classes = [
            AcademicClass(name='Licence 1', code='L1'),
            AcademicClass(name='Licence 2', code='L2'),
            AcademicClass(name='Licence 3', code='L3'),
            AcademicClass(name='Master 1', code='M1'),
            AcademicClass(name='Master 2', code='M2')
        ]
        for c in classes:
            db.session.add(c)
        db.session.flush()

        # Add Sample Schedules (for all days to make testing easy)
        for c in classes:
            for day in range(7): # Everyday
                s = Schedule(
                    class_id=c.id,
                    subject='Séance de test',
                    day_of_week=day,
                    start_time=time(8, 0),
                    end_time=time(18, 0),
                    room='Salle Virtuelle'
                )
                db.session.add(s)

        db.session.commit()
        click.echo("Database initialized with Super Admin (admin/admin123) and sample data.")
    else:
        click.echo("Database already initialized.")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
