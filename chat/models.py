from django.db import models

class ChatMessage(models.Model):
    title=models.Charfield(max_length=255)
    file=models.FileField(upload_to='documents/')
    uploaded_at=models.DateTimeField(auto_now_add=True)
    class Query(models.Model):
        text = models.TextField()
        response = models.TextField()
        created_at = models.DateTimeField(auto_now_add=True)
        