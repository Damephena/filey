from rest_framework import permissions


class IsFileOwnerOrAccessible(permissions.BasePermission):

    '''
    Object-level permission to only allow files flagged
    `is_accessible` to be seen by everyone.
    '''
    def has_object_permission(self, request, view, obj):
        message = 'File is not publically accessible.'

        return obj.owner == request.user or obj.is_accessible

class IsFileOwnerOrReadOnly(permissions.BasePermission):

    '''Object-level permission to only allow owners of a file to edit it.'''
    def has_object_permission(self, request, view, obj):
        message = 'Making changes to this file is not allowed.'

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user
