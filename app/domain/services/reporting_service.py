import pandas as pd
from app.domain.models.attendance import Attendance, Student
import io

class ReportingService:
    @staticmethod
    def generate_excel_report(session_id=None):
        """Generate an Excel report of attendance."""
        query = Attendance.query
        if session_id:
            query = query.filter_by(session_id=session_id)
            
        records = query.all()
        
        data = []
        for r in records:
            student = Student.query.get(r.student_id)
            data.append({
                'Matricule': student.student_id,
                'Nom': student.last_name,
                'Prénom': student.first_name,
                'Date/Heure': r.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'Statut': r.status,
                'Confiance': f"{r.confidence_score*100:.1f}%" if r.confidence_score else "N/A"
            })
            
        df = pd.DataFrame(data)
        
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Présences')
            
        output.seek(0)
        return output

    @staticmethod
    def generate_daily_summary():
        """Summary for institutional dashboard."""
        # Implementation for a general summary report
        pass
