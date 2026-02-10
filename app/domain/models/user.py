from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.domain.models.base import AuditMixin

class Role:
    SUPER_ADMIN = 'SUPER_ADMIN'
    FUNC_ADMIN = 'FUNC_ADMIN'
    TECH_USER = 'TECH_USER'

class User(db.Model, UserMixin, AuditMixin):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False, default=Role.FUNC_ADMIN)
    full_name = db.Column(db.String(100), nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def has_role(self, role):
        return self.role == role or self.role == Role.SUPER_ADMIN

    def __repr__(self):
        return f'<User {self.username} ({self.role})>'

class AuditLog(db.Model):
    __tablename__ = 'audit_log'
    
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    action = db.Column(db.String(100), nullable=False)
    module = db.Column(db.String(50), nullable=False)
    level = db.Column(db.String(20), default='INFO') # INFO, WARNING, ERROR, SECURITY
    details = db.Column(db.Text, nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)

    user = db.relationship('User', backref='actions')

    def __repr__(self):
        return f'<AuditLog {self.action} by {self.user_id}>'
