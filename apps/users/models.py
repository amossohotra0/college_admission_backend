from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager
from django.conf import settings
from django.core.exceptions import ValidationError

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)



class Role(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Principal/Admin'),
        ('admission_officer', 'Admission Officer'),
        ('data_entry', 'Data Entry Operator'),
        ('accountant', 'Accountant'),
        ('reviewer', 'Application Reviewer'),
        ('applicant', 'Student/Applicant'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, unique=True)
    group = models.OneToOneField(Group, on_delete=models.CASCADE, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_roles'
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='updated_roles'
    )

    def __str__(self):
        return self.role

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    cnic = models.CharField(max_length=15, blank=True)
    role = models.ForeignKey(Role, null=True, blank=True, on_delete=models.SET_NULL)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email} ({self.role})"

class StudentProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="student_profile")
    picture = models.ImageField(upload_to="students/pictures/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.get_full_name()

class PersonalInformation(models.Model):
    student = models.OneToOneField(StudentProfile, on_delete=models.CASCADE)
    father_name = models.CharField(max_length=100)
    cnic = models.CharField(max_length=15)
    registered_contact = models.CharField(max_length=20)
    cnic_front_img = models.ImageField(upload_to="students/cnic/front/")
    cnic_back_img = models.ImageField(upload_to="students/cnic/back/")
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[("male", "Male"), ("female", "Female"), ("other", "Other")])

class ContactInformation(models.Model):
    student = models.OneToOneField(StudentProfile, on_delete=models.CASCADE)
    district = models.CharField(max_length=100)
    tehsil = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    permanent_address = models.TextField()
    current_address = models.TextField()
    postal_address = models.TextField()

class StudentRelative(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="relatives")
    name = models.CharField(max_length=100)
    relationship = models.CharField(max_length=50)
    contact_one = models.CharField(max_length=20)
    contact_two = models.CharField(max_length=20, blank=True)
    address = models.TextField()

class Degree(models.Model):
    name = models.CharField(max_length=80, unique=True, blank=True)
    
    def __str__(self):
        return self.name or "Unnamed Degree"
    
class Institute(models.Model):
    name = models.CharField(max_length=80,unique=True, blank=True)
    
    def __str__(self):
        return self.name or "Unnamed Institute"
    
class EducationalBackground(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="educational_records")
    institution = models.ForeignKey(Institute, on_delete=models.CASCADE)
    degree = models.ForeignKey(Degree, on_delete=models.CASCADE)
    passing_year = models.PositiveIntegerField(blank=True)
    total_marks = models.PositiveIntegerField(blank=True)
    obtained_marks = models.PositiveIntegerField(blank=True)
    percentage = models.FloatField(blank=True)
    grade = models.CharField(max_length=10, blank=True)
    certificate = models.FileField(upload_to="students/certificates/")

    def save(self, *args, **kwargs):
        self.full_clean()
        if self.total_marks > 0:
            self.percentage = round((self.obtained_marks / self.total_marks) * 100, 2)
        super().save(*args, **kwargs)

    def clean(self):
        if self.obtained_marks > self.total_marks:
            raise ValidationError("Obtained marks cannot exceed total marks.")
    
    def __str__(self):
        return f"{self.student.user.email} - {self.degree.name} ({self.passing_year})"

class BloodGroup(models.Model):
    name = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"{self.name}"

class Disease(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.name}"

class MedicalInformation(models.Model):
    student = models.OneToOneField(StudentProfile, on_delete=models.CASCADE)
    blood_group = models.ForeignKey(BloodGroup, on_delete=models.CASCADE,null=True, blank=True)
    diseases = models.ManyToManyField(Disease)
    is_disabled = models.BooleanField(default=False)

    def __str__(self):
        return f"Medical Info for {self.student.user.email}"

