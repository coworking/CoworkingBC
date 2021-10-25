from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse


LOGIN_URL = "/login"


class WilmaLogin(LoginView):
    template_name = 'wilma/login.html'


class WilmaLogout(LogoutView):
    template_name = 'wilma/logout.html'


@login_required(login_url=LOGIN_URL)
def home(request):
    context = {
    }
    return render(request, 'wilma/home.html', context)
