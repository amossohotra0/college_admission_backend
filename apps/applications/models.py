from django.db import models
from django.utils import timezone
from django.conf import settings
from apps.users.models import CustomUser, StudentProfile
from apps.programs.models import Program, AcademicSession
from django.core.files.base import ContentFile
from model_utils import FieldTracker
import qrcode
from io import BytesIO
import uuid
import hashlib
from decouple import config
import os


class ApplicationStatus(models.Model):
    code = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
FRONT_END_URL = config('FRONT_END_URL')
VERIFICATION_URL = config('VERIFICATION_URL')

class Application(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='applications')
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    academic_session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)
    tracking_id = models.CharField(max_length=50, unique=True, editable=False)
    application_form_no = models.CharField(max_length=50, unique=True, editable=False)
    status = models.ForeignKey(ApplicationStatus, on_delete=models.SET_NULL, null=True, default=None)
    applied_at = models.DateTimeField(default=timezone.now)
    verification_hash = models.CharField(max_length=64, unique=True, editable=False)
    application_pdf = models.FileField(upload_to='applications/pdf/', blank=True, null=True)
    application_qrcode = models.ImageField(upload_to='applications/qrcodes/', blank=True, null=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='updated_applications'
    )
    
    # Track changes to the status field
    tracker = FieldTracker(['status_id'])

    def generate_verification_hash(self):
        raw_string = f"{self.tracking_id}{self.student.id}{self.program.id}{self.applied_at.timestamp()}"
        return hashlib.sha256(raw_string.encode()).hexdigest()

    def save(self, *args, **kwargs):
        is_new = self._state.adding

        if not self.tracking_id:
            uid = uuid.uuid4().hex[:10].upper()
            self.tracking_id = f"APP-{uid}"

        if not self.application_form_no:
            timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
            self.application_form_no = f"FORM-{timestamp}-{uuid.uuid4().hex[:6].upper()}"

        if is_new:
            super().save(*args, **kwargs)

        if not self.verification_hash:
            self.verification_hash = self.generate_verification_hash()
            super().save(update_fields=['verification_hash'])

        # Generate QR after hash is saved
        if not self.application_qrcode:
            qr_data = f"{VERIFICATION_URL}{self.verification_hash}"
            qr = qrcode.make(qr_data)
            buffer = BytesIO()
            qr.save(buffer, format="PNG")
            filename = f"{self.tracking_id}_qrcode.png"
            self.application_qrcode.save(filename, ContentFile(buffer.getvalue()), save=False)
            buffer.close()
            super().save(update_fields=['application_qrcode'])

    def __str__(self):
        return f"{self.student.user.email} - {self.program.name} ({self.status})"

class ApplicationApproved(models.Model):
    approved_app = models.OneToOneField(Application, on_delete=models.CASCADE, related_name='approval')
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='approved_applications')
    approved_at = models.DateTimeField(default=timezone.now)
    remarks = models.TextField(blank=True)

    def __str__(self):
        return f"{self.approved_app.tracking_id} approved by {self.approved_by.email}"

class ApplicationTracking(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='tracking_logs')
    status = models.ForeignKey(ApplicationStatus, on_delete=models.SET_NULL, null=True)
    remarks = models.TextField(blank=True)
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='status_updates'
    )
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.application.tracking_id} -> {self.status.name}"
    
class AdmissionLetter(models.Model):
    approved_application = models.OneToOneField(
        ApplicationApproved,
        on_delete=models.CASCADE,
        related_name='admission_letter'
    )
    merit_position = models.PositiveIntegerField(null=True, blank=True)
    issued_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='issued_admission_letters'
    )
    issued_at = models.DateTimeField(default=timezone.now)
    letter_pdf = models.FileField(upload_to='admissions/letters/pdf/', blank=True, null=True)

    def __str__(self):
        return f"Letter for {self.approved_application.approved_app.tracking_id}"
