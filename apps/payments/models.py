from django.db import models
from django.conf import settings
from django.utils import timezone
from apps.applications.models import Application

class FeeStructure(models.Model):
    program = models.ForeignKey('programs.Program', on_delete=models.CASCADE)
    session = models.ForeignKey('programs.AcademicSession', on_delete=models.CASCADE)
    application_fee = models.DecimalField(max_digits=10, decimal_places=2)
    admission_fee = models.DecimalField(max_digits=10, decimal_places=2)
    security_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ['program', 'session']
    
    def __str__(self):
        return f"{self.program.name} - {self.session.session}"

class PaymentMethod(models.Model):
    name = models.CharField(max_length=50)  # Bank Transfer, JazzCash, EasyPaisa, etc.
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class Payment(models.Model):
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    PAYMENT_TYPE = [
        ('application', 'Application Fee'),
        ('admission', 'Admission Fee'),
        ('security', 'Security Fee'),
    ]
    
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='payments')
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True)
    transaction_id = models.CharField(max_length=100, unique=True)
    bank_reference = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    paid_at = models.DateTimeField(null=True, blank=True)
    verified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    receipt = models.FileField(upload_to='payments/receipts/', blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.application.tracking_id} - {self.payment_type} - {self.amount}"