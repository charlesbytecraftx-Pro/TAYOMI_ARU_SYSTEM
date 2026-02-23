from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'group', 'date', 'time', 'location')
    list_filter = ('group', 'date')
    search_fields = ('title', 'location')