from django.db import models
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.db.models.signals import pre_save
from django.dispatch import receiver

User = get_user_model()

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    parent_message = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='replies',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"From {self.sender} to {self.receiver}: {self.content[:20]}"

class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='history')
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True) 
    edited_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='edited_histories')

    def __str__(self):
        return f"History for message {self.message.id} at {self.edited_at}"

class MessageHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageHistory
        fields = ['old_content', 'edited_at']

class MessageSerializer(serializers.ModelSerializer):
    history = MessageHistorySerializer(many=True, read_only=True)
    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'content', 'timestamp', 'edited', 'history']

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_message = Message.objects.get(pk=instance.pk)
            if old_message.content != instance.content:
                MessageHistory.objects.create(
                    message=instance,
                    old_content=old_message.content
                )
                instance.edited = True
        except Message.DoesNotExist:
            pass

# Example: Fetch all top-level messages and their replies for a conversation
messages = Message.objects.filter(parent_message__isnull=True).select_related('sender', 'receiver').prefetch_related('replies')

def get_threaded_replies(message):
    replies = message.replies.all().select_related('sender', 'receiver')
    result = []
    for reply in replies:
        result.append({
            'id': reply.id,
            'content': reply.content,
            'sender': reply.sender.username,
            'timestamp': reply.timestamp,
            'replies': get_threaded_replies(reply)
        })
    return result