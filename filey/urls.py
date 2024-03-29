"""filey URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path

import rest_framework.permissions as permissions
from dj_rest_auth.registration.views import VerifyEmailView
from dj_rest_auth.views import PasswordResetConfirmView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from .views import ping

schema_view = get_schema_view(
    openapi.Info(
        title = 'Filey API',
        default_version = 'v1',
        description = 'Filey application: A file storage application for users',
        terms_of_service = 'https://www.google.com/policies/terms/',
        contact=openapi.Contact(email='contact@snippets.local'),
        license=openapi.License(name='BSD License'),
    ),
    public = True,
    permission_classes = (permissions.AllowAny,),
)

urlpatterns = [
    path('', ping, name='ping'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('services/', include('services.urls')),

    path('auth/password/reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(),
            name='password_reset_confirm'),
    path('register/account-confirm-email/<key>/', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    path('drf/', include('rest_framework.urls')),
    path(r'auth/', include('dj_rest_auth.urls')),
    path('register/', include('dj_rest_auth.registration.urls')),

    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
