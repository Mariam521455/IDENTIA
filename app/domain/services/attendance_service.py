from datetime import datetime, time
from app import db
from app.domain.models.attendance import Attendance, Student
from app.domain.models.schedule import Schedule
from app.domain.services.audit_service import AuditService

class AttendanceService:
    @staticmethod
    def process_pointage(student_id):
        """Full process for recording attendance based on current schedule."""
        student = Student.query.get(student_id)
        if not student:
            return False, "Étudiant non reconnu"

        now = datetime.now()
        current_time = now.time()
        today = now.weekday() # 0-6

        # Find active schedule for this student's class
        schedule = Schedule.query.filter_by(class_id=student.class_id, day_of_week=today).first()
        
        # Security: In real production, we would check if now is within [start_time - 30m, end_time]
        if not schedule:
            return False, "Aucune séance prévue actuellement"

        # Check for duplicate pointage in the last 4 hours (simplified session management)
        # We assume one pointage per subject per day
        existing = Attendance.query.filter(
            Attendance.student_id == student.id,
            Attendance.timestamp >= datetime.combine(now.date(), time.min),
            Attendance.timestamp <= datetime.combine(now.date(), time.max)
        ).first()

        if existing:
            return False, "Déjà pointé aujourd'hui"

        # Determine if Late
        # Let's say more than 15 minutes late is 'LATE'
        start_dt = datetime.combine(now.date(), schedule.start_time)
        diff = (now - start_dt).total_seconds() / 60
        
        status = 'PRESENT'
        if diff > 15:
            status = 'LATE'
        elif diff < -30:
            return False, "Trop tôt pour pointer"

        attendance = Attendance(
            student_id=student.id,
            timestamp=now,
            status=status
        )
        
        db.session.add(attendance)
        db.session.commit()
        
        AuditService.log_action(
            action=f"Pointage {status}",
            module="RECOGNITION",
            details=f"Étudiant: {student.first_name} {student.last_name}, Heure: {now.strftime('%H:%M')}"
        )
        
        return True, status.lower() # Return status for the API to format

    @staticmethod
    def get_dashboard_stats():
        """Get summary stats for dashboard."""
        total_students = Student.query.count()
        today_start = datetime.combine(datetime.now().date(), time.min)
        
        today_attendance = Attendance.query.filter(
            Attendance.timestamp >= today_start
        ).count()
        
        late_today = Attendance.query.filter(
            Attendance.timestamp >= today_start,
            Attendance.status == 'LATE'
        ).count()
        
        rate = (today_attendance / total_students * 100) if total_students > 0 else 0
        
        return {
            'total_students': total_students,
            'attendance_rate': round(rate, 1),
            'present_count': today_attendance,
            'late_count': late_today,
            'classes_count': db.session.query(Student.class_id).distinct().count()
        }
