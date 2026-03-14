from django.db import models

class Traveler(models.Model):
    passport_number = models.CharField(max_length=20, unique=True, primary_key=True)
    name = models.CharField(max_length=255)
    nationality = models.CharField(max_length=100)
    dob = models.DateField()
    passport_expiry = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.passport_number})"

class EntryRecord(models.Model):
    STATUS_CHOICES = [
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('PENDING', 'Pending'),
    ]
    traveler = models.ForeignKey(Traveler, on_delete=models.CASCADE, related_name='entries')
    entry_time = models.DateTimeField(auto_now_add=True)
    border_location = models.CharField(max_length=100)
    officer_id = models.CharField(max_length=50)
    risk_score = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')

    def __str__(self):
        return f"Entry for {self.traveler.passport_number} at {self.border_location}"

class Blacklist(models.Model):
    traveler = models.OneToOneField(Traveler, on_delete=models.CASCADE, primary_key=True)
    reason = models.TextField()
    flag_level = models.IntegerField(default=1) # 1: Low, 2: Med, 3: High

    def __str__(self):
        return f"Blacklist: {self.traveler.passport_number}"

class VisaRecord(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('EXPIRED', 'Expired'),
        ('REVOKED', 'Revoked'),
    ]
    traveler = models.ForeignKey(Traveler, on_delete=models.CASCADE, related_name='visas')
    visa_type = models.CharField(max_length=50)
    expiry_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')

    def __str__(self):
        return f"Visa for {self.traveler.passport_number}"

