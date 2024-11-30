from django.db import models

class ChatMessage(models.Model):
    content = models.TextField()
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    sent_at = models.DateTimeField(auto_now_add=True)

"""class FailedLoginAttempt(models.Model):
    username = models.CharField(max_length=150)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)"""
