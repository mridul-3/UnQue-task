from rest_framework import permissions

class IsProfessor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'professor'

class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'student'

class IsOwnerOrProfessor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.user_type == 'professor':
            return obj.professor == request.user
        elif request.user.user_type == 'student':
            return obj.student == request.user
        return False

