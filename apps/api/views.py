from rest_framework import generics, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q, Count
from django.utils import timezone
from apps.common.permissions import *
from apps.users.models import *
from apps.programs.models import *
from apps.applications.models import *
from apps.payments.models import *
from apps.dashboard.models import *
from .serializers import *
import uuid

# ==================== AUTHENTICATION VIEWS ====================
class RegisterView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "Registration successful. Please complete your profile to apply for admission.",
        }, status=status.HTTP_201_CREATED)

class UserProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    
    def get_object(self):
        return self.request.user

# ==================== STUDENT PROFILE MANAGEMENT ====================
class StudentProfileViewSet(viewsets.ModelViewSet):
    serializer_class = StudentProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.role.role == 'applicant':
            return StudentProfile.objects.filter(user=self.request.user)
        return StudentProfile.objects.all()
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get', 'post', 'put'], permission_classes=[IsApplicant])
    def my_profile(self, request):
        try:
            profile = StudentProfile.objects.get(user=request.user)
            if request.method == 'GET':
                serializer = StudentProfileSerializer(profile)
                return Response(serializer.data)
            elif request.method in ['POST', 'PUT']:
                serializer = StudentProfileSerializer(profile, data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data)
        except StudentProfile.DoesNotExist:
            if request.method == 'POST':
                serializer = StudentProfileSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

class PersonalInformationView(generics.CreateAPIView, generics.RetrieveUpdateAPIView):
    serializer_class = PersonalInformationSerializer
    permission_classes = [IsApplicant]
    
    def get_object(self):
        profile = get_object_or_404(StudentProfile, user=self.request.user)
        return get_object_or_404(PersonalInformation, student=profile)
    
    def perform_create(self, serializer):
        profile, created = StudentProfile.objects.get_or_create(user=self.request.user)
        serializer.save(student=profile)

class ContactInformationView(generics.CreateAPIView, generics.RetrieveUpdateAPIView):
    serializer_class = ContactInformationSerializer
    permission_classes = [IsApplicant]
    
    def get_object(self):
        profile = get_object_or_404(StudentProfile, user=self.request.user)
        return get_object_or_404(ContactInformation, student=profile)
    
    def perform_create(self, serializer):
        profile, created = StudentProfile.objects.get_or_create(user=self.request.user)
        serializer.save(student=profile)

class StudentRelativeViewSet(viewsets.ModelViewSet):
    serializer_class = StudentRelativeSerializer
    permission_classes = [IsApplicant]
    
    def get_queryset(self):
        profile = get_object_or_404(StudentProfile, user=self.request.user)
        return StudentRelative.objects.filter(student=profile)
    
    def perform_create(self, serializer):
        profile, created = StudentProfile.objects.get_or_create(user=self.request.user)
        serializer.save(student=profile)

class EducationalBackgroundViewSet(viewsets.ModelViewSet):
    serializer_class = EducationalBackgroundSerializer
    permission_classes = [IsApplicant]
    
    def get_queryset(self):
        profile = get_object_or_404(StudentProfile, user=self.request.user)
        return EducationalBackground.objects.filter(student=profile)
    
    def perform_create(self, serializer):
        profile, created = StudentProfile.objects.get_or_create(user=self.request.user)
        serializer.save(student=profile)

class MedicalInformationView(generics.CreateAPIView, generics.RetrieveUpdateAPIView):
    serializer_class = MedicalInformationSerializer
    permission_classes = [IsApplicant]
    
    def get_object(self):
        profile = get_object_or_404(StudentProfile, user=self.request.user)
        return get_object_or_404(MedicalInformation, student=profile)
    
    def perform_create(self, serializer):
        profile, created = StudentProfile.objects.get_or_create(user=self.request.user)
        serializer.save(student=profile)

# ==================== PROGRAM MANAGEMENT ====================
class ProgramViewSet(viewsets.ModelViewSet):
    queryset = Program.objects.filter(is_deleted=False)
    serializer_class = ProgramSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsAdmissionOfficer]
        return [permission() for permission in permission_classes]

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.filter(is_deleted=False)
    serializer_class = CourseSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsAdmissionOfficer]
        return [permission() for permission in permission_classes]

class AcademicSessionViewSet(viewsets.ModelViewSet):
    queryset = AcademicSession.objects.all()
    serializer_class = AcademicSessionSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsAdmissionOfficer]
        return [permission() for permission in permission_classes]

class OfferedProgramViewSet(viewsets.ModelViewSet):
    queryset = OfferedProgram.objects.filter(is_active=True)
    serializer_class = OfferedProgramSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsAdmissionOfficer]
        return [permission() for permission in permission_classes]

# ==================== APPLICATION MANAGEMENT ====================
class ApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer
    
    def get_queryset(self):
        if self.request.user.role.role == 'applicant':
            profile = get_object_or_404(StudentProfile, user=self.request.user)
            return Application.objects.filter(student=profile)
        return Application.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ApplicationCreateSerializer
        return ApplicationSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsApplicant]
        elif self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [CanManageApplications]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        profile = get_object_or_404(StudentProfile, user=self.request.user)
        submitted_status = ApplicationStatus.objects.get(code='submitted')
        application = serializer.save(student=profile, status=submitted_status)
        
        # Create application fee payment record
        fee_structure = FeeStructure.objects.filter(
            program=application.program,
            session=application.academic_session,
            is_active=True
        ).first()
        
        if fee_structure:
            Payment.objects.create(
                application=application,
                payment_type='application',
                amount=fee_structure.application_fee,
                transaction_id=f"APP-{uuid.uuid4().hex[:8].upper()}"
            )
    
    @action(detail=True, methods=['post'], permission_classes=[CanManageApplications])
    def update_status(self, request, pk=None):
        application = self.get_object()
        serializer = ApplicationStatusUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        new_status = get_object_or_404(ApplicationStatus, id=serializer.validated_data['status_id'])
        old_status = application.status
        
        application.status = new_status
        application.updated_by = request.user
        application.save()
        
        # Create tracking log
        ApplicationTracking.objects.create(
            application=application,
            status=new_status,
            remarks=serializer.validated_data.get('remarks', ''),
            changed_by=request.user
        )
        
        # If approved, create admission fee payment
        if new_status.code == 'approved':
            fee_structure = FeeStructure.objects.filter(
                program=application.program,
                session=application.academic_session,
                is_active=True
            ).first()
            
            if fee_structure:
                Payment.objects.get_or_create(
                    application=application,
                    payment_type='admission',
                    defaults={
                        'amount': fee_structure.admission_fee,
                        'transaction_id': f"ADM-{uuid.uuid4().hex[:8].upper()}"
                    }
                )
        
        return Response({
            'message': f'Status updated from {old_status.name} to {new_status.name}',
            'application': ApplicationSerializer(application).data
        })
    
    @action(detail=True, methods=['get'])
    def tracking(self, request, pk=None):
        application = self.get_object()
        tracking_logs = ApplicationTracking.objects.filter(application=application).order_by('-timestamp')
        serializer = ApplicationTrackingSerializer(tracking_logs, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[CanViewReports])
    def statistics(self, request):
        stats = Application.objects.values('status__name').annotate(count=Count('id'))
        return Response(stats)

# ==================== PAYMENT MANAGEMENT ====================
class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    
    def get_queryset(self):
        if self.request.user.role.role == 'applicant':
            profile = get_object_or_404(StudentProfile, user=self.request.user)
            return Payment.objects.filter(application__student=profile)
        return Payment.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return PaymentCreateSerializer
        return PaymentSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        elif self.action == 'create':
            permission_classes = [IsApplicant]
        else:
            permission_classes = [IsAccountant]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        payment = serializer.save()
        payment.transaction_id = f"PAY-{uuid.uuid4().hex[:8].upper()}"
        payment.save()
    
    @action(detail=True, methods=['post'], permission_classes=[IsAccountant])
    def verify_payment(self, request, pk=None):
        payment = self.get_object()
        payment.status = 'paid'
        payment.paid_at = timezone.now()
        payment.verified_by = request.user
        payment.save()
        
        return Response({
            'message': 'Payment verified successfully',
            'payment': PaymentSerializer(payment).data
        })

class FeeStructureViewSet(viewsets.ModelViewSet):
    queryset = FeeStructure.objects.filter(is_active=True)
    serializer_class = FeeStructureSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsAdmissionOfficer]
        return [permission() for permission in permission_classes]

class PaymentMethodViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PaymentMethod.objects.filter(is_active=True)
    serializer_class = PaymentMethodSerializer
    permission_classes = [permissions.IsAuthenticated]

# ==================== DASHBOARD & REPORTS ====================
class AnnouncementViewSet(viewsets.ModelViewSet):
    serializer_class = AnnouncementSerializer
    
    def get_queryset(self):
        if self.request.user.role.role == 'applicant':
            return Announcement.objects.filter(
                Q(target_roles=self.request.user.role) | Q(target_roles__isnull=True),
                is_active=True
            )
        return Announcement.objects.filter(is_active=True)
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsAdmissionOfficer]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class AdmissionStatsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AdmissionStats.objects.all()
    serializer_class = AdmissionStatsSerializer
    permission_classes = [CanViewReports]

# ==================== LOOKUP DATA ====================
class DegreeViewSet(viewsets.ModelViewSet):
    queryset = Degree.objects.all()
    serializer_class = DegreeSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsDataEntry]
        return [permission() for permission in permission_classes]

class InstituteViewSet(viewsets.ModelViewSet):
    queryset = Institute.objects.all()
    serializer_class = InstituteSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsDataEntry]
        return [permission() for permission in permission_classes]

class BloodGroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BloodGroup.objects.all()
    serializer_class = BloodGroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class DiseaseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Disease.objects.all()
    serializer_class = DiseaseSerializer
    permission_classes = [permissions.IsAuthenticated]

class ApplicationStatusViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ApplicationStatus.objects.all()
    serializer_class = ApplicationStatusSerializer
    permission_classes = [CanManageApplications]

class RoleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAdminUser]