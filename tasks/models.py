from django.db import models
from django.contrib.auth.models import User 

class Task(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="tasks",
        null=True, 
        blank=True
    )
    
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    
    # The "Soft Delete" fix
    is_archived = models.BooleanField(default=False) 
    
    # The "Chart Memory" fix - use DateTimeField to match timezone.now()
    completed_at = models.DateTimeField(null=True, blank=True)

    priority = models.CharField(
        max_length=10, 
        choices=[('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')], 
        default='Medium'
    )

    due_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username if self.user else 'Public'}: {self.title}"