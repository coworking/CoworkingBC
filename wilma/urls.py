"""wilma URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path

from wilma import xero_auth

urlpatterns = [
    path('admin/', admin.site.urls),

    # Xero OAuth2 URLs
    path('xero/', xero_auth.start_xero_auth),
    path('xero/auth', xero_auth.process_callback),
    path('xero/test', xero_auth.test_xero_auth),
]
