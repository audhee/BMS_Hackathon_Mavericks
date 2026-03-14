from django.urls import path
from .views import VerifyTravelerView, TravelerDetailView, EntryRecordCreateView

urlpatterns = [
    path('verify-traveler/', VerifyTravelerView.as_view(), name='verify_traveler'),
    path('traveler/<str:passport_number>/', TravelerDetailView.as_view(), name='traveler_detail'),
    path('entry/', EntryRecordCreateView.as_view(), name='entry_record_create'),
]
