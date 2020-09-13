from rest_framework import permissions

class UpdateOwnData(permissions.BasePermission):
    """Allow users to their own data"""
    def has_object_permission(self,request,view,obj):
        """Check user is trying their own data"""
        return obj.id == request.user.id

class IsResturantOwner(permissions.BasePermission):
    """Allow users to their own data"""
    def has_object_permission(self,request,view,obj):
        """Check user is trying their own data"""
        return obj.owner.id == request.user.id


class UpdateOwnAddress(permissions.BasePermission):
    """Allow users to their own data"""
    def has_object_permission(self,request,view,obj):
        """Check user is trying their own data"""
        return obj.user_profile.id == request.user.id

class AdminOnlyApi(permissions.BasePermission):
    """Permission check for apis only available to admins"""

    def has_permission(self,request,view):
        """Check if user is admin"""
        return request.user.is_staff

class UpdateAdminOnly(permissions.BasePermission):
    """Permission check for apis only updateable or creatable by admins"""

    def has_object_permission(self,request,view,obj):
        """Check if user is admin"""
        return request.user.is_staff