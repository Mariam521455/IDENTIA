import face_recognition
import numpy as np
import io
import base64
import cv2
from app import db
from app.domain.models.attendance import FacialEncoding, Student

class RecognitionService:
    @staticmethod
    def get_encoding_from_image(image_path_or_file):
        """Extract facial encoding from an image."""
        image = face_recognition.load_image_file(image_path_or_file)
        encodings = face_recognition.face_encodings(image)
        if encodings:
            return encodings[0]
        return None

    @staticmethod
    def _base64_to_image(base64_string):
        """Convert base64 image data to a format face_recognition can use."""
        if ',' in base64_string:
            base64_string = base64_string.split(',')[1]
        img_data = base64.b64decode(base64_string)
        return face_recognition.load_image_file(io.BytesIO(img_data))

    @staticmethod
    def enroll_student(student_db_id, images_dict):
        """
        Enroll a student with multiple angles.
        images_dict: {'front': base64, 'left': base64, 'right': base64}
        """
        student = Student.query.get(student_db_id)
        if not student:
            return False, "Étudiant introuvable"

        encodings_count = 0
        for angle, b64_data in images_dict.items():
            if not b64_data:
                continue
                
            try:
                image = RecognitionService._base64_to_image(b64_data)
                encodings = face_recognition.face_encodings(image)
                
                if encodings:
                    encoding_bytes = encodings[0].tobytes()
                    
                    # Save multi-angle encoding
                    facial_enc = FacialEncoding(
                        student_id=student.id,
                        encoding=encoding_bytes,
                        angle_type=angle
                    )
                    db.session.add(facial_enc)
                    
                    # Set primary encoding if front
                    if angle == 'front':
                        student.face_encoding = encoding_bytes
                    
                    encodings_count += 1
            except Exception as e:
                print(f"Error enrolling angle {angle}: {e}")
        
        if encodings_count > 0:
            student.is_enrolled = True
            db.session.commit()
            return True, f"{encodings_count} angles enregistrés avec succès"
        
        return False, "Aucun visage détecté dans les images fournies"

    @staticmethod
    def identify_face(base64_frame, tolerance=0.5):
        """Identify a student from a real-time video frame."""
        try:
            image = RecognitionService._base64_to_image(base64_frame)
            face_locations = face_recognition.face_locations(image)
            face_encodings = face_recognition.face_encodings(image, face_locations)
            
            if not face_encodings:
                return None, 0.0

            # Get all enrolled students' encodings
            all_encodings = FacialEncoding.query.all()
            if not all_encodings:
                return None, 0.0

            # Use the find_match utility
            student_id, confidence = RecognitionService.find_match(face_encodings[0], all_encodings, tolerance)
            if student_id:
                return Student.query.get(student_id), confidence
                
        except Exception as e:
            print(f"Error during identification: {e}")
            
        return None, 0.0
