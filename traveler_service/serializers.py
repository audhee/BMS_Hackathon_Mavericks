from rest_framework import serializers
from .models import Traveler, EntryRecord, Blacklist, VisaRecord

class TravelerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Traveler
        fields = '__all__'

class EntryRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntryRecord
        fields = '__all__'

class BlacklistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blacklist
        fields = '__all__'

class VisaRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisaRecord
        fields = '__all__'
