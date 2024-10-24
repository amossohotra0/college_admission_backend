from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from apps.users.models import *
from apps.applications.models import ApplicationStatus
from apps.programs.models import *
from apps.payments.models import *


class Command(BaseCommand):
    help = 'Setup initial data for the application'

    def handle(self, *args, **options):
        self.stdout.write('Setting up initial data...')
        
        # Create roles
        roles_data = [
            ('admin', 'Principal/Admin'),
            ('admission_officer', 'Admission Officer'),
            ('data_entry', 'Data Entry Operator'),
            ('accountant', 'Accountant'),
            ('reviewer', 'Application Reviewer'),
            ('applicant', 'Student/Applicant'),
        ]
        
        for role_code, role_name in roles_data:
            group, created = Group.objects.get_or_create(name=role_name)
            role, created = Role.objects.get_or_create(
                role=role_code,
                defaults={'group': group}
            )
            if created:
                self.stdout.write(f'Created role: {role_name}')
        
        # Create application statuses
        statuses_data = [
            ('submitted', 'Submitted', 'Application has been submitted'),
            ('under_review', 'Under Review', 'Application is being reviewed'),
            ('approved', 'Approved', 'Application has been approved'),
            ('rejected', 'Rejected', 'Application has been rejected'),
            ('waitlisted', 'Waitlisted', 'Application is on waitlist'),
        ]
        
        for code, name, description in statuses_data:
            status, created = ApplicationStatus.objects.get_or_create(
                code=code,
                defaults={'name': name, 'description': description}
            )
            if created:
                self.stdout.write(f'Created status: {name}')
        
        # Create sample degrees
        degrees = ['Matric', 'Intermediate', 'Bachelor', 'Master', 'PhD']
        for degree_name in degrees:
            degree, created = Degree.objects.get_or_create(name=degree_name)
            if created:
                self.stdout.write(f'Created degree: {degree_name}')
        
        # Create sample institutes
        institutes = ['Government High School', 'Government College', 'University of Punjab', 'LUMS', 'NUST']
        for institute_name in institutes:
            institute, created = Institute.objects.get_or_create(name=institute_name)
            if created:
                self.stdout.write(f'Created institute: {institute_name}')
        
        # Create blood groups
        blood_groups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
        for bg in blood_groups:
            blood_group, created = BloodGroup.objects.get_or_create(name=bg)
            if created:
                self.stdout.write(f'Created blood group: {bg}')
        
        # Create sample diseases
        diseases = ['Diabetes', 'Hypertension', 'Asthma', 'Heart Disease', 'None']
        for disease_name in diseases:
            disease, created = Disease.objects.get_or_create(name=disease_name)
            if created:
                self.stdout.write(f'Created disease: {disease_name}')
        
        # Create sample courses
        courses_data = [
            ('CS101', 'Computer Science'),
            ('EE101', 'Electrical Engineering'),
            ('ME101', 'Mechanical Engineering'),
            ('BBA101', 'Business Administration'),
        ]
        
        for code, name in courses_data:
            course, created = Course.objects.get_or_create(
                code=code,
                defaults={'name': name}
            )
            if created:
                self.stdout.write(f'Created course: {name}')
        
        # Create sample programs
        programs_data = [
            ('BSCS', 'Bachelor of Science in Computer Science'),
            ('BSEE', 'Bachelor of Science in Electrical Engineering'),
            ('BSME', 'Bachelor of Science in Mechanical Engineering'),
            ('BBA', 'Bachelor of Business Administration'),
        ]
        
        for code, name in programs_data:
            program, created = Program.objects.get_or_create(
                code=code,
                defaults={'name': name}
            )
            if created:
                self.stdout.write(f'Created program: {name}')
        
        # Create current academic session
        from datetime import date
        current_year = date.today().year
        session, created = AcademicSession.objects.get_or_create(
            start_date=date(current_year, 9, 1),
            end_date=date(current_year + 1, 8, 31),
            defaults={'is_current': True}
        )
        if created:
            self.stdout.write(f'Created academic session: {session.session}')
        
        # Create payment methods
        payment_methods = ['Bank Transfer', 'JazzCash', 'EasyPaisa', 'HBL Konnect', 'Cash']
        for method_name in payment_methods:
            method, created = PaymentMethod.objects.get_or_create(name=method_name)
            if created:
                self.stdout.write(f'Created payment method: {method_name}')
        
        # Create fee structures for programs
        for program in Program.objects.all():
            for session in AcademicSession.objects.all():
                fee_structure, created = FeeStructure.objects.get_or_create(
                    program=program,
                    session=session,
                    defaults={
                        'application_fee': 1000,  # PKR 1000
                        'admission_fee': 15000,   # PKR 15000
                        'security_fee': 5000,     # PKR 5000
                    }
                )
                if created:
                    self.stdout.write(f'Created fee structure for {program.name} - {session.session}')
        
        # Create sample users for different roles
        users_data = [
            ('admin@college.edu', 'admin', 'Principal', 'Admin', 'admin123', True, True),
            ('admission@college.edu', 'admission_officer', 'Admission', 'Officer', 'admission123', True, False),
            ('accountant@college.edu', 'accountant', 'Finance', 'Officer', 'account123', True, False),
            ('reviewer@college.edu', 'reviewer', 'Application', 'Reviewer', 'review123', True, False),
            ('student@example.com', 'applicant', 'Test', 'Student', 'student123', False, False),
        ]
        
        for email, role_code, first_name, last_name, password, is_staff, is_superuser in users_data:
            role = Role.objects.get(role=role_code)
            user, created = CustomUser.objects.get_or_create(
                email=email,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'role': role,
                    'is_staff': is_staff,
                    'is_superuser': is_superuser,
                    'is_verified': True
                }
            )
            if created:
                user.set_password(password)
                user.save()
                self.stdout.write(f'Created user: {email} (password: {password})')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully set up initial data')
        )