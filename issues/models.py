from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Issue(models.Model):
    STATUS_CHOICES = [
        ('Pending Implementation', 'Pending Implementation'),
        ('In Progress', 'In Progress'),
        ('Ready for UAT', 'Ready for UAT'),
        ('Ready to Deploy', 'Ready to Deploy'),
        ('Done', 'Done'),
    ]

    title = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    assignee = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending Implementation')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Update closed_at field based on status change
        if self.status == 'Done' and self.closed_at is None:
            self.closed_at = timezone.now()
        elif self.status != 'Done':
            self.closed_at = None

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
