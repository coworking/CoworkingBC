from django.urls import path
from django.contrib import admin
from django.views.generic.base import RedirectView

from wilma import views


urlpatterns = [
    path('favicon.ico', RedirectView.as_view(url='/static/img/favicon-32x32.png', permanent=True)),
    path('robots.txt', lambda r: HttpResponse("User-agent: *\nDisallow: /", content_type="text/plain")),

    path('', views.home, name='home'),
    path('login/', views.WilmaLogin.as_view(), name='wilma_login'),
    path('logout/', views.WilmaLogout.as_view(), name='wilma_logout'),
    path('xero/', views.xero_start_auth),
    path('xero/auth', views.xero_callback),
    path('xero_contacts', views.xero_contacts, name='xero_contacts'),

    path('admin/', admin.site.urls),
]
