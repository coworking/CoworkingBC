from django.urls import path
from django.contrib import admin
from django.views.generic.base import RedirectView

from wilma import views, xero_auth


urlpatterns = [
    path('favicon.ico', RedirectView.as_view(url='/static/img/favicon-32x32.png', permanent=True)),
    path('robots.txt', lambda r: HttpResponse("User-agent: *\nDisallow: /", content_type="text/plain")),

    path('', views.home, name='home'),
    path('login/', views.WilmaLogin.as_view(), name='wilma_login'),
    path('logout/', views.WilmaLogout.as_view(), name='wilma_logout'),

    # Xero OAuth2 URLs
    path('xero/', xero_auth.start_xero_auth),
    path('xero/auth', xero_auth.process_callback),
    path('xero/test', xero_auth.test_xero_auth),

    path('admin/', admin.site.urls),
]
