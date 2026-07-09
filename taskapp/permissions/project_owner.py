from rest_framework import permissions

class IsProjectOwnerOrTaskAssignee(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):

        if obj.project.owner == request.user:
            return True
            
        if request.method in permissions.SAFE_METHODS:
            return obj.assigned_user == request.user
            
        return False