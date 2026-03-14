from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from .models import Traveler, EntryRecord, Blacklist, VisaRecord
from .serializers import TravelerSerializer, EntryRecordSerializer, BlacklistSerializer, VisaRecordSerializer
from .services import AIServiceClient

class VerifyTravelerView(APIView):
    def get(self, request):
        return Response({
            "message": "This endpoint requires a POST request with passport_image and live_face_image."
        })

    def post(self, request):
        passport_image = request.data.get('passport_image')
        live_face_image = request.data.get('live_face_image')
        border_location = request.data.get('border_location', 'Unknown')
        officer_id = request.data.get('officer_id', 'Unknown')

        if not passport_image or not live_face_image:
            return Response({"error": "Images required."}, status=status.HTTP_400_BAD_REQUEST)

        # 1. OCR Service
        ocr_result = AIServiceClient.call_ocr(passport_image)
        passport_number = ocr_result.get('passport_number')
        
        if not passport_number:
            return Response({"error": "Failed to extract passport number."}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        # 2. Face Match Service
        face_match_result = AIServiceClient.call_face_match(passport_image, live_face_image)

        # 3. Check DB for Traveler Records
        traveler = Traveler.objects.filter(passport_number=passport_number).first()
        blacklist_entry = Blacklist.objects.filter(traveler__passport_number=passport_number).first()
        visa_entry = VisaRecord.objects.filter(traveler__passport_number=passport_number).first()

        # 4. Consolidate data for Risk Assessment
        risk_data = {
            "passport_number": passport_number,
            "ocr_result": ocr_result,
            "face_match_confidence": face_match_result.get('match_confidence'),
            "on_blacklist": blacklist_entry is not None,
            "visa_status": visa_entry.status if visa_entry else "No Visa"
        }

        # 5. Risk Assessment Service
        risk_result = AIServiceClient.call_risk_assessment(risk_data)

        # 6. Build final status
        final_status = "APPROVED" if risk_result.get('risk_score', 100) < 50 else "REJECTED"

        # 7. AUTOMATIC REGISTRATION & LOGGING
        # If the traveler is fair (Approved) but missing from DB, we register them!
        if final_status == "APPROVED" and not traveler:
            traveler = Traveler.objects.create(
                passport_number=passport_number,
                name=ocr_result.get('name'),
                nationality=ocr_result.get('nationality'),
                dob=ocr_result.get('dob'),
                passport_expiry=ocr_result.get('passport_expiry')
            )
            print(f"Registered new traveler: {traveler.name}")

        # Record every entry attempt in the history logs
        if traveler: # We only log if we have a traveler record (existing or just created)
            EntryRecord.objects.create(
                traveler=traveler,
                border_location=border_location,
                officer_id=officer_id,
                risk_score=risk_result.get('risk_score'),
                status=final_status
            )

        # 8. Build final response
        response_data = {
            "traveler": ocr_result,
            "verification": face_match_result,
            "database_signals": {
                "blacklist_level": blacklist_entry.flag_level if blacklist_entry else 0,
                "visa_status": visa_entry.status if visa_entry else "NOT_FOUND"
            },
            "risk_score": risk_result.get('risk_score'),
            "status": final_status,
            "auto_registered": not traveler # True if we just created them
        }

        return Response(response_data, status=status.HTTP_200_OK)

class TravelerDetailView(APIView):
    def get(self, request, passport_number):
        traveler = Traveler.objects.filter(passport_number=passport_number).first()
        if not traveler:
            return Response({"error": "Traveler not found."}, status=status.HTTP_404_NOT_FOUND)
        
        entries = EntryRecord.objects.filter(traveler=traveler).order_by('-entry_time')
        
        return Response({
            "traveler": TravelerSerializer(traveler).data,
            "history": EntryRecordSerializer(entries, many=True).data
        })

class EntryRecordCreateView(CreateAPIView):
    queryset = EntryRecord.objects.all()
    serializer_class = EntryRecordSerializer

