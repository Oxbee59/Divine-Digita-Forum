from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/login/', permanent=False)),
    path('admin/', admin.site.urls),
    path('', include('forum.urls')),
]

# 🔥 FORCE Django to serve media ALWAYS (needed on Render)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
