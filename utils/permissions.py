from rest_framework import permissions


class IsFileOwnerOrAccessible(permissions.BasePermission):

    '''Object-level permission to only allow owners of a file to edit it.'''
    def has_object_permission(self, request, view, obj):
        message = 'Making changes to this file is not allowed. File is not publically accessible.'

        if obj.is_accessible:
            return True

        return obj.owner == request.user
