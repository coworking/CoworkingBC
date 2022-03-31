from django.urls import path
from django.http import HttpResponse
from django.contrib import admin

from wilma import views


urlpatterns = [
    path('robots.txt', lambda r: HttpResponse("User-agent: *\nDisallow: /", content_type="text/plain")),

    path('', views.home, name='home'),
    path('login/', views.WilmaLogin.as_view(), name='wilma_login'),
    path('logout/', views.WilmaLogout.as_view(), name='wilma_logout'),
    path('xero/', views.xero_start_auth, name='xero_auth'),
    path('xero/auth', views.xero_callback),
    path('xero/contacts', views.xero_contacts, name='xero_contacts'),

    path('admin/', admin.site.urls),
]
