from django.db import models
from django.utils import timezone
from django.conf import settings

class Course(models.Model):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=15, blank=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_courses'
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='updated_courses'
    )

    def __str__(self):
        return f"{self.name} ({self.code})"


class Program(models.Model):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=15, blank=True)
    courses = models.ManyToManyField(Course, related_name='programs')
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_programs'
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='updated_programs'
    )

    def __str__(self):
        return f"{self.name} ({self.code})"

class AcademicSession(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    session = models.CharField(max_length=9, unique=True, blank=True)
    is_current = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_session'
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='updated_session'
    )

    def save(self, *args, **kwargs):
        self.session = f"{self.start_date.year}-{self.end_date.year}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.session


class OfferedProgram(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='offerings')
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE, related_name='offered_programs')
    total_seats = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_offered_programs'
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='updated_offered_program'
    )

    def __str__(self):
        return f"{self.program.name} ({self.session.session})"
