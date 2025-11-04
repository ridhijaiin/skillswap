from django.contrib import admin
from django.urls import path, include
from accounts import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Home page
    path('', views.home, name="home"),

    # Accounts app routes
    path('', include('accounts.urls')),
    # Include default Django auth views (login/logout/password management)
    path('accounts/', include('django.contrib.auth.urls')),
]

# Media files (uploads)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
