from django.contrib import admin
from .models import Traveler, EntryRecord, Blacklist, VisaRecord

@admin.register(Traveler)
class TravelerAdmin(admin.ModelAdmin):
    list_display = ('passport_number', 'name', 'nationality', 'passport_expiry')
    search_fields = ('passport_number', 'name')

@admin.register(EntryRecord)
class EntryRecordAdmin(admin.ModelAdmin):
    list_display = ('traveler', 'entry_time', 'border_location', 'risk_score', 'status')
    list_filter = ('status', 'border_location')
    search_fields = ('traveler__passport_number', 'officer_id')

@admin.register(Blacklist)
class BlacklistAdmin(admin.ModelAdmin):
    list_display = ('traveler', 'reason', 'flag_level')

@admin.register(VisaRecord)
class VisaRecordAdmin(admin.ModelAdmin):
    list_display = ('traveler', 'visa_type', 'expiry_date', 'status')
    list_filter = ('status', 'visa_type')
