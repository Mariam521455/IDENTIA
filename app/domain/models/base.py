from datetime import datetime
from app import db

class AuditMixin:
    """Mixin for audit fields in every table."""
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=True)

    def soft_delete(self, user_id):
        self.is_deleted = True
        self.deleted_at = datetime.utcnow()
        # In a real app, user_id recording would be here too
        db.session.commit()
