from django.db import models
from django.conf import settings  # Ongeza hii

class Group(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        related_name='tayomi_groups', 
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Leadership(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='leaders')
    # Badilisha 'User' iwe settings.AUTH_USER_MODEL hapa pia
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    position = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user} - {self.position} ({self.group.name})"