import os
import django
import sys

# Set up Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'border_backend.settings')
django.setup()

from traveler_service.models import Traveler, Blacklist, VisaRecord, EntryRecord
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from datetime import date, timedelta

def seed_data():
    print("Seeding data...")
    
    # 0. Create Auth User for Officers
    user, created = User.objects.get_or_create(
        username="admin",
        defaults={"is_staff": True, "is_superuser": True}
    )
    if created:
        user.set_password("admin@123")
        user.save()
        print(f"Created Admin User: {user.username}")
    
    # Generate token for admin
    token, _ = Token.objects.get_or_create(user=user)
    print(f"Admin Token: {token.key}")
    
    # 1. Create a normal traveler (The "Safe" Case)
    t1, created = Traveler.objects.get_or_create(
        passport_number="X12345678",
        defaults={
            "name": "John Doe",
            "nationality": "USA",
            "dob": date(1990, 1, 1),
            "passport_expiry": date(2030, 1, 1)
        }
    )
    if created: print(f"Created Traveler: {t1.name}")

    # Add an active visa for John
    VisaRecord.objects.get_or_create(
        traveler=t1,
        visa_type="Business",
        defaults={
            "expiry_date": date.today() + timedelta(days=365),
            "status": "ACTIVE"
        }
    )

    # 2. Create a blacklisted traveler (The "Danger" Case)
    t2, created = Traveler.objects.get_or_create(
        passport_number="B99999999",
        defaults={
            "name": "Jane Doe",
            "nationality": "Unknown",
            "dob": date(1985, 5, 5),
            "passport_expiry": date(2025, 5, 5)
        }
    )
    if created: print(f"Created Traveler: {t2.name}")

    Blacklist.objects.get_or_create(
        traveler=t2,
        defaults={
            "reason": "Security Alert - Interpol Watchlist",
            "flag_level": 3
        }
    )

    # 3. Create a traveler with an EXPIRED visa (The "Caution" Case)
    t3, created = Traveler.objects.get_or_create(
        passport_number="E55555555",
        defaults={
            "name": "Bob Smith",
            "nationality": "UK",
            "dob": date(1978, 10, 20),
            "passport_expiry": date(2028, 10, 20)
        }
    )
    if created: print(f"Created Traveler: {t3.name}")

    VisaRecord.objects.get_or_create(
        traveler=t3,
        visa_type="Tourist",
        defaults={
            "expiry_date": date.today() - timedelta(days=10), # Expired 10 days ago
            "status": "EXPIRED"
        }
    )

    # 4. Add some history for John
    EntryRecord.objects.get_or_create(
        traveler=t1,
        border_location="Delhi Airport (IGI)",
        defaults={
            "officer_id": "OFFICER_007",
            "risk_score": 10,
            "status": "APPROVED"
        }
    )

    print("Seeding complete! Ready for demo.")

if __name__ == "__main__":
    seed_data()
