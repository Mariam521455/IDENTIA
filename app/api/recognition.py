from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required
from app.domain.services.recognition_service import RecognitionService
from app.domain.services.attendance_service import AttendanceService
from app import db
from app.domain.models.attendance import Student, FacialEncoding
from app.domain.models.schedule import AcademicClass

recognition_bp = Blueprint('recognition', __name__)

@recognition_bp.route('/enroll', methods=['GET', 'POST'])
def enroll():
    if request.method == 'POST':
        data = request.json
        
        # 1. Create Student
        student = Student(
            student_id=data.get('matricule'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            major=data.get('major'),
            class_id=data.get('class_id')
        )
        db.session.add(student)
        db.session.flush() # Get student.id
        
        # 2. Process Encodings
        images = {
            'front': data.get('image_front'),
            'left': data.get('image_left'),
            'right': data.get('image_right')
        }
        
        success, message = RecognitionService.enroll_student(student.id, images)
        
        if success:
            db.session.commit()
            return jsonify({"status": "success", "message": "Étudiant enrôlé avec succès"})
        else:
            db.session.rollback()
            return jsonify({"status": "error", "message": message}), 400
            
    classes = AcademicClass.query.all()
    return render_template('enrollment.html', classes=classes)

@recognition_bp.route('/identify', methods=['POST'])
def identify():
    data = request.json
    image_b64 = data.get('image')
    
    if not image_b64:
        return jsonify({"status": "error", "message": "Aucune image reçue"}), 400
        
    # 1. Recognize the face
    student, confidence = RecognitionService.identify_face(image_b64)
    
    if not student:
        return jsonify({
            "status": "refused", 
            "name": "Inconnu",
            "message": "Accès Refusé - Visage non reconnu"
        })
        
    # 2. Process Pointage
    success, status_or_msg = AttendanceService.process_pointage(student.id)
    
    label = "Présent"
    if status_or_msg == 'late': label = "En retard"
    
    if success:
        return jsonify({
            "status": "success", 
            "name": f"{student.first_name} {student.last_name}",
            "message": label
        })
    else:
        # If failure (e.g. duplicate or too early), we still show the name but error message
        return jsonify({
            "status": "error",
            "name": f"{student.first_name} {student.last_name}",
            "message": status_or_msg # "Déjà pointé", etc.
        })

@recognition_bp.route('/pointage')
def pointage():
    return render_template('pointage.html')
