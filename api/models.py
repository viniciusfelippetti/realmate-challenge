import uuid
from django.db import models

class Conversation(models.Model):
    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('CLOSED', 'Closed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=6, choices=STATUS_CHOICES, default='OPEN')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} - {self.status}"

class Message(models.Model):
    TYPE_CHOICES = [
        ('SENT', 'Sent'),
        ('RECEIVED', 'Received'),
    ]

    id = models.UUIDField(primary_key=True)
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    direction = models.CharField(max_length=8, choices=TYPE_CHOICES)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.direction}: {self.content[:30]}"
