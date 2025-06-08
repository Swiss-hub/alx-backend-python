#!/usr/bin/env python3
"""
Custom permissions for messaging_app.chats.
"""

from rest_framework import permissions
from .models import Conversation

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to allow only authenticated users who are participants
    of a conversation to view, send, update, or delete messages.
    """

    def has_permission(self, request, view):
        # Require authentication globally
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Object-level permission:
        Only participants of the conversation can access.
        - obj is typically a Message or Conversation instance.
        """
        # If checking a Conversation object
        if isinstance(obj, Conversation):
            return request.user in obj.participants.all()

        # If checking a Message object — assume it has a 'conversation' FK
        return request.user in obj.conversation.participants.all()
