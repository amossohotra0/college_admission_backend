from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """Principal/Admin access"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role and request.user.role.role == 'admin'

class IsAdmissionOfficer(permissions.BasePermission):
    """Admission Officer and above"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role and request.user.role.role in ['admin', 'admission_officer']

class IsReviewer(permissions.BasePermission):
    """Application reviewers and above"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role and request.user.role.role in ['admin', 'admission_officer', 'reviewer']

class IsAccountant(permissions.BasePermission):
    """Accountant and above for payment operations"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role and request.user.role.role in ['admin', 'accountant']

class IsDataEntry(permissions.BasePermission):
    """Data entry operator and above"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role and request.user.role.role in ['admin', 'admission_officer', 'data_entry']

class IsApplicant(permissions.BasePermission):
    """Student/Applicant access"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role and request.user.role.role == 'applicant'

class IsOwnerOrStaff(permissions.BasePermission):
    """Owner or staff member access"""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.READONLY_METHODS:
            return True
        return (obj.user == request.user or 
                request.user.role.role in ['admin', 'admission_officer', 'data_entry'])

class CanManageApplications(permissions.BasePermission):
    """Can manage application status"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role and request.user.role.role in ['admin', 'admission_officer', 'reviewer']

class CanViewReports(permissions.BasePermission):
    """Can view reports and statistics"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role and request.user.role.role in ['admin', 'admission_officer']