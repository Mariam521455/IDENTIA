from app import db
from app.domain.models.user import AuditLog
from flask import request
from flask_login import current_user
import datetime

class AuditService:
    @staticmethod
    def log_action(action, module, details=None, level='INFO'):
        """Professional audit logging for every institutional action."""
        user_id = current_user.id if current_user.is_authenticated else None
        
        log_entry = AuditLog(
            user_id=user_id,
            action=action,
            module=module,
            details=details,
            level=level,
            ip_address=request.remote_addr if request else "Local",
            timestamp=datetime.datetime.utcnow()
        )
        
        try:
            db.session.add(log_entry)
            db.session.commit()
        except Exception as e:
            # Fallback to local file logging if DB fails
            print(f"CRITICAL: Failed to write audit log to DB: {e}")
            with open("logs/emergency_audit.log", "a") as f:
                f.write(f"{datetime.datetime.utcnow()} - {action} - {module} - {user_id} - {details}\n")

    @staticmethod
    def log_security_event(action, details):
        """Specific logging for security-related events."""
        AuditService.log_action(action, 'SECURITY', details, level='SECURITY')
