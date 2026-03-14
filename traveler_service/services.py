import requests
import json

class AIServiceClient:
    OCR_URL = "http://ai-service/ocr"
    FACE_MATCH_URL = "http://ai-service/face-match"
    RISK_ASSESSMENT_URL = "http://ai-service/risk-assessment"

    @staticmethod
    def call_ocr(passport_image):
        # MOCK LOGIC FOR DEMO
        img_name = str(passport_image).lower()
        if "blacklisted" in img_name:
            return {"passport_number": "B99999999", "name": "Jane Doe", "nationality": "Unknown", "dob": "1985-05-05", "passport_expiry": "2025-05-05"}
        elif "expired" in img_name:
            return {"passport_number": "E55555555", "name": "Bob Smith", "nationality": "UK", "dob": "1978-10-20", "passport_expiry": "2028-10-20"}
        elif "first_time" in img_name:
            return {"passport_number": "N77777777", "name": "Sarah Miller", "nationality": "Canada", "dob": "1995-03-12", "passport_expiry": "2035-03-12"}
        else:
            return {"passport_number": "X12345678", "name": "John Doe", "nationality": "USA", "dob": "1990-01-01", "passport_expiry": "2030-01-01"}

    @staticmethod
    def call_face_match(passport_image, live_face_image):
        try:
            confidence = 98.5
            if "blacklisted" in str(passport_image).lower(): confidence = 45.0
            return {"match_confidence": confidence, "verified": confidence > 80}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def call_risk_assessment(data):
        try:
            score = 15
            # 1. Blacklist check (Critical)
            if data.get("on_blacklist"):
                score = 95
            # 2. Expired Visa (Violation)
            elif data.get("visa_status") == "EXPIRED":
                score = 75
            # 3. NO Visa (First Timer / Visa-on-Arrival)
            elif data.get("visa_status") == "No Visa":
                score = 30  # MODERATE BUT APPROVED
            # 4. Biometric Suspicion
            elif data.get("face_match_confidence", 100) < 70:
                score = 80
            
            return {
                "risk_score": score, 
                "assessment": "High Risk" if score >= 50 else "Low Risk",
                "status_note": "First-time entry detected" if score == 30 else "Normal"
            }
        except Exception as e:
            return {"error": str(e)}
