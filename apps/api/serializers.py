from rest_framework import serializers
from apps.users.models import *
from apps.programs.models import *
from apps.applications.models import *
from apps.payments.models import *
from apps.dashboard.models import *

# User & Authentication Serializers
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'role']

class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'phone', 'cnic', 'role', 'is_verified']
        read_only_fields = ['id', 'is_verified']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'phone', 'cnic', 'password', 'password2']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = CustomUser.objects.create_user(**validated_data)
        # Assign applicant role by default
        applicant_role, _ = Role.objects.get_or_create(role='applicant')
        user.role = applicant_role
        user.save()
        return user

# Student Profile Serializers
class PersonalInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalInformation
        fields = '__all__'
        read_only_fields = ['student']

class ContactInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInformation
        fields = '__all__'
        read_only_fields = ['student']

class StudentRelativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentRelative
        fields = '__all__'
        read_only_fields = ['student']

class EducationalBackgroundSerializer(serializers.ModelSerializer):
    institution_name = serializers.CharField(source='institution.name', read_only=True)
    degree_name = serializers.CharField(source='degree.name', read_only=True)
    
    class Meta:
        model = EducationalBackground
        fields = '__all__'
        read_only_fields = ['student', 'percentage']

class MedicalInformationSerializer(serializers.ModelSerializer):
    blood_group_name = serializers.CharField(source='blood_group.name', read_only=True)
    diseases_list = serializers.StringRelatedField(source='diseases', many=True, read_only=True)
    
    class Meta:
        model = MedicalInformation
        fields = '__all__'
        read_only_fields = ['student']

class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    personal_info = PersonalInformationSerializer(source='personalinformation', read_only=True)
    contact_info = ContactInformationSerializer(source='contactinformation', read_only=True)
    relatives = StudentRelativeSerializer(many=True, read_only=True)
    educational_records = EducationalBackgroundSerializer(many=True, read_only=True)
    medical_info = MedicalInformationSerializer(source='medicalinformation', read_only=True)
    profile_completion = serializers.SerializerMethodField()
    
    class Meta:
        model = StudentProfile
        fields = '__all__'
        read_only_fields = ['user']
    
    def get_profile_completion(self, obj):
        completion = 0
        if hasattr(obj, 'personalinformation'):
            completion += 25
        if hasattr(obj, 'contactinformation'):
            completion += 25
        if obj.educational_records.exists():
            completion += 25
        if hasattr(obj, 'medicalinformation'):
            completion += 25
        return completion

# Program Serializers
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name', 'code', 'is_active']

class ProgramSerializer(serializers.ModelSerializer):
    courses = CourseSerializer(many=True, read_only=True)
    
    class Meta:
        model = Program
        fields = ['id', 'name', 'code', 'courses', 'is_active']

class AcademicSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicSession
        fields = ['id', 'session', 'start_date', 'end_date', 'is_current']

class OfferedProgramSerializer(serializers.ModelSerializer):
    program = ProgramSerializer(read_only=True)
    session = AcademicSessionSerializer(read_only=True)
    available_seats = serializers.SerializerMethodField()
    
    class Meta:
        model = OfferedProgram
        fields = '__all__'
    
    def get_available_seats(self, obj):
        approved_count = Application.objects.filter(
            program=obj.program,
            academic_session=obj.session,
            status__code='approved'
        ).count()
        return obj.total_seats - approved_count

# Application Serializers
class ApplicationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationStatus
        fields = '__all__'

class ApplicationSerializer(serializers.ModelSerializer):
    student = StudentProfileSerializer(read_only=True)
    program = ProgramSerializer(read_only=True)
    session = AcademicSessionSerializer(source='academic_session', read_only=True)
    status = ApplicationStatusSerializer(read_only=True)
    can_apply = serializers.SerializerMethodField()
    payment_status = serializers.SerializerMethodField()
    
    class Meta:
        model = Application
        fields = '__all__'
        read_only_fields = ['tracking_id', 'application_form_no', 'verification_hash']
    
    def get_can_apply(self, obj):
        # Check if student profile is complete
        student = obj.student
        return (hasattr(student, 'personalinformation') and 
                hasattr(student, 'contactinformation') and
                student.educational_records.exists())
    
    def get_payment_status(self, obj):
        payments = obj.payments.filter(payment_type='application')
        if payments.exists():
            return payments.first().status
        return 'not_paid'

class ApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['program', 'academic_session']
    
    def validate(self, attrs):
        request = self.context['request']
        student_profile = StudentProfile.objects.filter(user=request.user).first()
        
        if not student_profile:
            raise serializers.ValidationError("Please complete your profile first")
        
        # Check profile completion
        if not (hasattr(student_profile, 'personalinformation') and 
                hasattr(student_profile, 'contactinformation') and
                student_profile.educational_records.exists() and
                hasattr(student_profile, 'medicalinformation')):
            raise serializers.ValidationError("Please complete all profile sections before applying")
        
        # Check if already applied
        existing = Application.objects.filter(
            student=student_profile,
            program=attrs['program'],
            academic_session=attrs['academic_session']
        ).exists()
        
        if existing:
            raise serializers.ValidationError("You have already applied for this program")
        
        return attrs

# Payment Serializers
class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = '__all__'

class FeeStructureSerializer(serializers.ModelSerializer):
    program = ProgramSerializer(read_only=True)
    session = AcademicSessionSerializer(read_only=True)
    
    class Meta:
        model = FeeStructure
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    application = ApplicationSerializer(read_only=True)
    payment_method = PaymentMethodSerializer(read_only=True)
    
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ['transaction_id', 'verified_by']

class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['application', 'payment_type', 'amount', 'payment_method', 'bank_reference', 'receipt']

# Dashboard Serializers
class AnnouncementSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    target_roles = RoleSerializer(many=True, read_only=True)
    
    class Meta:
        model = Announcement
        fields = '__all__'

class AdmissionStatsSerializer(serializers.ModelSerializer):
    program = ProgramSerializer(read_only=True)
    session = AcademicSessionSerializer(read_only=True)
    
    class Meta:
        model = AdmissionStats
        fields = '__all__'

# Lookup Serializers
class DegreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Degree
        fields = '__all__'

class InstituteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institute
        fields = '__all__'

class BloodGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = BloodGroup
        fields = '__all__'

class DiseaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disease
        fields = '__all__'

# Status Update Serializers
class ApplicationStatusUpdateSerializer(serializers.Serializer):
    status_id = serializers.IntegerField()
    remarks = serializers.CharField(required=False, allow_blank=True)

class ApplicationTrackingSerializer(serializers.ModelSerializer):
    status = ApplicationStatusSerializer(read_only=True)
    changed_by = UserSerializer(read_only=True)
    
    class Meta:
        model = ApplicationTracking
        fields = '__all__'