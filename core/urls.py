from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Django Admin Panel
    path('admin/', admin.site.urls),
    
    # Members (Login, Dashboard, nk.)
    path('', include('accounts.urls')), 
    
    # Malipo na Admin Panel ya TAYOMI
    path('payments/', include('payments.urls')),
    
    # Groups
    path('groups/', include('groups.urls')),
    # Events
    path('events/', include('events.urls')),
]

# Ruhusu picha/mafaili (Media & Static) 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
