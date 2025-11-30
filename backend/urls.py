from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    # Root redirects to login page
    path('', RedirectView.as_view(url='/login/', permanent=False)),

    # Django admin
    path('admin/', admin.site.urls),

    # Your app URLs
    path('', include('forum.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
