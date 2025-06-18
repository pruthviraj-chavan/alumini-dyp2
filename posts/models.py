from django.db import models
from django.conf import settings

class Post(models.Model):
    """Base model for all types of posts (achievements, job opportunities)"""
    
    class Category(models.TextChoices):
        ACHIEVEMENT = 'ACHIEVEMENT', 'Achievement'
        JOB = 'JOB', 'Job Opportunity'
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    category = models.CharField(max_length=20, choices=Category.choices)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.get_category_display()} by {self.user.email}"
