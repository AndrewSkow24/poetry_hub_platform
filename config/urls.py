# core/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import RedirectView
from poem.views import SignUpView

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='poem:list', permanent=False), name='home'),
    path('admin/', admin.site.urls),
    path('poems/', include('poem.urls')),
    path('login/', LoginView.as_view(
        template_name='registration/login.html',
        redirect_authenticated_user=True
    ), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)