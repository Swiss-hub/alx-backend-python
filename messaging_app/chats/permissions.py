#!/usr/bin/env python3
"""
Custom permissions for messaging_app.chats.
"""

from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow users to access their own chats/messages.
    """

    def has_object_permission(self, request, view, obj):
        # Assuming obj has a user or owner field
        return obj.user == request.user
