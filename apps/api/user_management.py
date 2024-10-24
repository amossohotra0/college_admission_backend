from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import Group
from apps.common.permissions import IsAdminUser
from apps.users.models import CustomUser, Role
from .serializers import UserSerializer, RoleSerializer

class UserManagementViewSet(viewsets.ModelViewSet):
    """
    API endpoint for user management (admin only)
    """
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    
    def get_queryset(self):
        return CustomUser.objects.all().order_by('-date_joined')
    
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        user = self.get_object()
        user.is_active = True
        user.save()
        return Response({'status': 'user activated'})
    
    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        user = self.get_object()
        user.is_active = False
        user.save()
        return Response({'status': 'user deactivated'})
    
    @action(detail=True, methods=['post'])
    def change_role(self, request, pk=None):
        user = self.get_object()
        try:
            role_id = request.data.get('role_id')
            role = Role.objects.get(id=role_id)
            user.role = role
            user.save()
            return Response({'status': 'role updated', 'role': RoleSerializer(role).data})
        except Role.DoesNotExist:
            return Response({'error': 'Role not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)