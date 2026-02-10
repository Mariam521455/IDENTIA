from app import db
from app.domain.models.base import AuditMixin
from datetime import datetime

class Student(db.Model, AuditMixin):
    __tablename__ = 'student'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(20), unique=True, nullable=False, index=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    # Biometric data (facial encoding stored as binary blob)
    face_encoding = db.Column(db.LargeBinary, nullable=True)
    
    attendances = db.relationship('Attendance', backref='student', lazy='dynamic')

    def __repr__(self):
        return f'<Student {self.first_name} {self.last_name}>'

class Classroom(db.Model, AuditMixin):
    __tablename__ = 'classroom'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    description = db.Column(db.String(256))
    
    sessions = db.relationship('AttendanceSession', backref='classroom', lazy='dynamic')

class AttendanceSession(db.Model, AuditMixin):
    __tablename__ = 'attendance_session'
    
    id = db.Column(db.Integer, primary_key=True)
    classroom_id = db.Column(db.Integer, db.ForeignKey('classroom.id'), nullable=False)
    title = db.Column(db.String(128), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    
    records = db.relationship('Attendance', backref='session', lazy='dynamic')

class Attendance(db.Model, AuditMixin):
    __tablename__ = 'attendance'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey('attendance_session.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Audit trail for biometric match
    confidence_score = db.Column(db.Float, nullable=True)
    status = db.Column(db.String(20), default='PRESENT') # PRESENT, LATE, ABSENT
    
    def __repr__(self):
        return f'<Attendance Student:{self.student_id} Session:{self.session_id}>'
