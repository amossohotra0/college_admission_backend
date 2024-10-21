# Data Seeding Guide

## Overview
This guide explains how to populate the College Admission Management System with sample data for development and testing.

## Automatic Seeding

### Quick Setup
```bash
python manage.py setup_initial_data
```

This command automatically creates all necessary data including roles, users, programs, and lookup data.

## Manual Seeding

### 1. Create Custom Management Command

Create a new seeding command:
```bash
mkdir -p apps/common/management/commands
```

Create `apps/common/management/commands/seed_sample_data.py`:
```python
from django.core.management.base import BaseCommand
from apps.users.models import *
from apps.programs.models import *
from apps.applications.models import *
from apps.payments.models import *

class Command(BaseCommand):
    help = 'Seed database with sample data'

    def handle(self, *args, **options):
        self.create_sample_students()
        self.create_sample_applications()
        self.stdout.write(self.style.SUCCESS('Sample data created successfully'))

    def create_sample_students(self):
        # Create sample students with complete profiles
        pass

    def create_sample_applications(self):
        # Create sample applications
        pass
```

### 2. Using Django Shell

```bash
python manage.py shell
```

#### Create Sample Students
```python
from apps.users.models import *
from apps.programs.models import *

# Create student user
applicant_role = Role.objects.get(role='applicant')
student = CustomUser.objects.create_user(
    email='ahmed.ali@example.com',
    first_name='Ahmed',
    last_name='Ali',
    phone='03001234567',
    cnic='12345-1234567-1',
    role=applicant_role
)

# Create student profile
profile = StudentProfile.objects.create(
    user=student,
    picture='path/to/picture.jpg'
)

# Add personal information
PersonalInformation.objects.create(
    student=profile,
    father_name='Ali Ahmed',
    cnic='12345-1234567-1',
    registered_contact='03001234567',
    date_of_birth='2000-05-15',
    gender='male'
)

# Add contact information
ContactInformation.objects.create(
    student=profile,
    district='Lahore',
    tehsil='Model Town',
    city='Lahore',
    permanent_address='House 123, Street 1, Model Town',
    current_address='House 123, Street 1, Model Town',
    postal_address='House 123, Street 1, Model Town'
)

# Add educational background
matric_degree = Degree.objects.get(name='Matric')
govt_school = Institute.objects.get(name='Government High School')

EducationalBackground.objects.create(
    student=profile,
    institution=govt_school,
    degree=matric_degree,
    passing_year=2018,
    total_marks=1100,
    obtained_marks=950,
    grade='A'
)
```

#### Create Sample Applications
```python
from apps.applications.models import *

# Get required objects
cs_program = Program.objects.get(code='BSCS')
current_session = AcademicSession.objects.get(is_current=True)
submitted_status = ApplicationStatus.objects.get(code='submitted')

# Create application
application = Application.objects.create(
    student=profile,
    program=cs_program,
    academic_session=current_session,
    status=submitted_status
)
```

## Sample Data Sets

### 1. Student Data
```python
SAMPLE_STUDENTS = [
    {
        'email': 'ahmed.ali@example.com',
        'first_name': 'Ahmed',
        'last_name': 'Ali',
        'phone': '03001234567',
        'cnic': '12345-1234567-1',
        'personal_info': {
            'father_name': 'Ali Ahmed',
            'date_of_birth': '2000-05-15',
            'gender': 'male'
        },
        'contact_info': {
            'district': 'Lahore',
            'city': 'Lahore',
            'permanent_address': 'House 123, Model Town'
        }
    },
    {
        'email': 'fatima.khan@example.com',
        'first_name': 'Fatima',
        'last_name': 'Khan',
        'phone': '03009876543',
        'cnic': '54321-7654321-2',
        'personal_info': {
            'father_name': 'Khan Sahib',
            'date_of_birth': '2001-03-20',
            'gender': 'female'
        },
        'contact_info': {
            'district': 'Karachi',
            'city': 'Karachi',
            'permanent_address': 'Flat 456, Gulshan'
        }
    }
]
```

### 2. Program Data
```python
SAMPLE_PROGRAMS = [
    {
        'name': 'Bachelor of Science in Software Engineering',
        'code': 'BSSE',
        'courses': ['Programming', 'Database', 'Software Design']
    },
    {
        'name': 'Bachelor of Commerce',
        'code': 'BCOM',
        'courses': ['Accounting', 'Economics', 'Business Studies']
    }
]
```

### 3. Application Scenarios
```python
APPLICATION_SCENARIOS = [
    {
        'student_email': 'ahmed.ali@example.com',
        'program_code': 'BSCS',
        'status': 'approved',
        'payment_status': 'paid'
    },
    {
        'student_email': 'fatima.khan@example.com',
        'program_code': 'BBA',
        'status': 'under_review',
        'payment_status': 'pending'
    }
]
```

## Advanced Seeding Script

Create `apps/common/management/commands/seed_complete_data.py`:

```python
from django.core.management.base import BaseCommand
from django.db import transaction
from apps.users.models import *
from apps.programs.models import *
from apps.applications.models import *
from apps.payments.models import *
import random
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Seed database with comprehensive sample data'

    def add_arguments(self, parser):
        parser.add_argument('--students', type=int, default=50, help='Number of students to create')
        parser.add_argument('--applications', type=int, default=100, help='Number of applications to create')

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        students_count = options['students']
        applications_count = options['applications']
        
        self.create_students(students_count)
        self.create_applications(applications_count)
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {students_count} students and {applications_count} applications')
        )

    def create_students(self, count):
        applicant_role = Role.objects.get(role='applicant')
        
        for i in range(count):
            # Create user
            user = CustomUser.objects.create_user(
                email=f'student{i+1}@example.com',
                first_name=f'Student{i+1}',
                last_name='Test',
                phone=f'0300{1000000 + i}',
                cnic=f'{10000 + i}-{1000000 + i}-{i % 9 + 1}',
                role=applicant_role
            )
            
            # Create profile
            profile = StudentProfile.objects.create(user=user)
            
            # Add personal info
            PersonalInformation.objects.create(
                student=profile,
                father_name=f'Father of Student{i+1}',
                cnic=f'{10000 + i}-{1000000 + i}-{i % 9 + 1}',
                registered_contact=f'0300{1000000 + i}',
                date_of_birth=date(2000 + i % 5, (i % 12) + 1, (i % 28) + 1),
                gender=random.choice(['male', 'female'])
            )
            
            # Add contact info
            cities = ['Lahore', 'Karachi', 'Islamabad', 'Faisalabad', 'Multan']
            ContactInformation.objects.create(
                student=profile,
                district=random.choice(cities),
                tehsil=f'Tehsil {i+1}',
                city=random.choice(cities),
                permanent_address=f'House {i+1}, Street {i+1}',
                current_address=f'House {i+1}, Street {i+1}',
                postal_address=f'House {i+1}, Street {i+1}'
            )
            
            # Add educational background
            degrees = Degree.objects.all()
            institutes = Institute.objects.all()
            
            EducationalBackground.objects.create(
                student=profile,
                institution=random.choice(institutes),
                degree=random.choice(degrees),
                passing_year=2018 + (i % 5),
                total_marks=1100,
                obtained_marks=800 + (i % 300),
                grade=random.choice(['A', 'B', 'C'])
            )

    def create_applications(self, count):
        students = StudentProfile.objects.all()
        programs = Program.objects.all()
        sessions = AcademicSession.objects.all()
        statuses = ApplicationStatus.objects.all()
        
        for i in range(count):
            student = random.choice(students)
            program = random.choice(programs)
            session = random.choice(sessions)
            status = random.choice(statuses)
            
            # Check if application already exists
            if not Application.objects.filter(
                student=student,
                program=program,
                academic_session=session
            ).exists():
                Application.objects.create(
                    student=student,
                    program=program,
                    academic_session=session,
                    status=status
                )
```

## Run Seeding Commands

### Basic Seeding
```bash
python manage.py setup_initial_data
```

### Advanced Seeding
```bash
python manage.py seed_complete_data --students 100 --applications 200
```

### Custom Seeding
```bash
python manage.py seed_sample_data
```

## Data Verification

### Check Created Data
```bash
python manage.py shell
```

```python
from apps.users.models import *
from apps.applications.models import *

# Check users count
print(f"Total users: {CustomUser.objects.count()}")
print(f"Students: {CustomUser.objects.filter(role__role='applicant').count()}")

# Check applications
print(f"Total applications: {Application.objects.count()}")
print(f"Approved applications: {Application.objects.filter(status__code='approved').count()}")

# Check profiles completion
profiles_with_personal_info = StudentProfile.objects.filter(personalinformation__isnull=False).count()
print(f"Profiles with personal info: {profiles_with_personal_info}")
```

## Reset and Re-seed

### Clear All Data
```bash
python manage.py flush --noinput
python manage.py migrate
python manage.py setup_initial_data
```

### Clear Specific Data
```python
# In Django shell
from apps.applications.models import Application
from apps.users.models import StudentProfile, CustomUser

# Clear applications
Application.objects.all().delete()

# Clear student profiles (keeps users)
StudentProfile.objects.all().delete()

# Clear all applicant users
CustomUser.objects.filter(role__role='applicant').delete()
```

## Production Considerations

### Environment-Specific Seeding
```python
# In management command
from django.conf import settings

if settings.DEBUG:
    # Only seed in development
    self.create_sample_data()
else:
    self.stdout.write('Skipping seeding in production')
```

### Large Dataset Seeding
```python
# Use bulk_create for better performance
users_to_create = []
for i in range(1000):
    users_to_create.append(CustomUser(
        email=f'user{i}@example.com',
        first_name=f'User{i}'
    ))

CustomUser.objects.bulk_create(users_to_create, batch_size=100)
```

This seeding system provides flexible data population for development, testing, and demonstration purposes.