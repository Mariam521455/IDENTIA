from app import db
from app.domain.models.base import AuditMixin
from datetime import time

class AcademicClass(db.Model, AuditMixin):
    __tablename__ = 'academic_class'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    
    students = db.relationship('Student', backref='academic_class', lazy='dynamic')
    schedules = db.relationship('Schedule', backref='academic_class', lazy='dynamic')

    def __repr__(self):
        return f'<AcademicClass {self.name}>'

class Schedule(db.Model, AuditMixin):
    __tablename__ = 'schedule'
    
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('academic_class.id'), nullable=False)
    subject = db.Column(db.String(128), nullable=False)
    day_of_week = db.Column(db.Integer, nullable=False) # 0-6 (Monday-Sunday)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    room = db.Column(db.String(64))
    
    def __repr__(self):
        return f'<Schedule {self.subject} ({self.day_of_week})>'
