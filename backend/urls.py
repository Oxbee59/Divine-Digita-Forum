from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
import os

urlpatterns = [
    # Root redirects to login page
    path('', RedirectView.as_view(url='/login/', permanent=False)),

    # Django admin
    path('admin/', admin.site.urls),

    # Your app URLs
    path('', include('forum.urls')),
]

# Serve media files in development or when explicitly enabled via env var SERVE_MEDIA=True
if settings.DEBUG or os.environ.get('SERVE_MEDIA', 'False') == 'True':
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
