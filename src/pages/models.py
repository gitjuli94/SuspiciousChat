from django.db import models

class ChatMessage(models.Model):
    content = models.TextField()
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    sent_at = models.DateTimeField(auto_now_add=True)
