import face_recognition
import numpy as np
import cv2
from app.domain.models.attendance import Student
from app import db

class FaceRecognitionService:
    @staticmethod
    def get_encoding(image_path):
        """Extracts face encodings from an image."""
        try:
            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)
            if encodings:
                # Return the first face found as a binary blob
                return encodings[0].tobytes()
            return None
        except Exception as e:
            # In a real app, use the logging service here
            print(f"Error in encoding extraction: {e}")
            return None

    @staticmethod
    def identify_face(frame, known_students, tolerance=0.6):
        """
        Identifies a face from a camera frame against a list of known student encodings.
        known_students: List of Student objects with face_encoding blobs.
        """
        # Convert BGR (OpenCV) to RGB (face_recognition)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Find all faces in current frame
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        results = []
        
        for face_encoding in face_encodings:
            matches = []
            distances = []
            
            for student in known_students:
                if student.face_encoding:
                    # Convert blob back to numpy array
                    known_encoding = np.frombuffer(student.face_encoding, dtype=np.float64)
                    
                    # Compare
                    match = face_recognition.compare_faces([known_encoding], face_encoding, tolerance=tolerance)
                    distance = face_recognition.face_distance([known_encoding], face_encoding)
                    
                    if match[0]:
                        matches.append(student)
                        distances.append(distance[0])

            if matches:
                # Find the best match
                best_match_idx = np.argmin(distances)
                results.append({
                    'student': matches[best_match_idx],
                    'confidence': 1 - distances[best_match_idx],
                    'location': face_locations
                })
            else:
                results.append({
                    'student': None,
                    'confidence': 0,
                    'location': face_locations
                })
                
        return results

    @staticmethod
    def validate_image_quality(image_path):
        """Place holder for institution-level image quality checks (brightness, focus)."""
        return True
