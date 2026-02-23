from django.db import models
from groups.models import Group
from accounts.models import CustomUser

class Event(models.Model):
    image = models.ImageField(upload_to='event_banners/', null=True, blank=True)
    group = models.ForeignKey('groups.Group', on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.group.name}"
