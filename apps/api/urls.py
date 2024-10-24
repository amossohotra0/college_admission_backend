from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *
from .user_management import UserManagementViewSet

# Create router for ViewSets
router = DefaultRouter()

# Student Management
router.register(r'students', StudentProfileViewSet, basename='student')
router.register(r'student-relatives', StudentRelativeViewSet, basename='student-relative')
router.register(r'educational-background', EducationalBackgroundViewSet, basename='educational-background')

# Program Management
router.register(r'programs', ProgramViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'academic-sessions', AcademicSessionViewSet)
router.register(r'offered-programs', OfferedProgramViewSet)

# Application Management
router.register(r'applications', ApplicationViewSet, basename='application')
router.register(r'application-statuses', ApplicationStatusViewSet)

# Payment Management
router.register(r'payments', PaymentViewSet, basename='payment')
router.register(r'fee-structures', FeeStructureViewSet)
router.register(r'payment-methods', PaymentMethodViewSet)

# Dashboard & Reports
router.register(r'announcements', AnnouncementViewSet, basename='announcement')
router.register(r'admission-stats', AdmissionStatsViewSet)

# Lookup Data
router.register(r'degrees', DegreeViewSet)
router.register(r'institutes', InstituteViewSet)
router.register(r'blood-groups', BloodGroupViewSet)
router.register(r'diseases', DiseaseViewSet)
router.register(r'roles', RoleViewSet)

# User Management
router.register(r'users', UserManagementViewSet, basename='user-management')

urlpatterns = [
    # OpenAPI Documentation
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # Authentication Endpoints
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/profile/', UserProfileView.as_view(), name='profile'),
    
    # Student Profile Management
    path('profile/personal-info/', PersonalInformationView.as_view(), name='personal-info'),
    path('profile/contact-info/', ContactInformationView.as_view(), name='contact-info'),
    path('profile/medical-info/', MedicalInformationView.as_view(), name='medical-info'),
    
    # Include router URLs
    path('', include(router.urls)),
]