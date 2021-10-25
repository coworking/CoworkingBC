import logging

from xero import Xero
from xero.auth import OAuth2Credentials
from xero.constants import XeroScopes

from django.conf import settings
from django.core.cache import caches
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse


LOGIN_URL = "/login"


class WilmaLogin(LoginView):
    template_name = 'wilma/login.html'


class WilmaLogout(LogoutView):
    template_name = 'wilma/logout.html'


@staff_member_required
def home(request):
    context = {
    }
    return render(request, 'wilma/home.html', context)


######################################################################
# Xero Views
######################################################################

@staff_member_required
def xero_start_auth(request):
    client_id = settings.XERO_CLIENT_ID
    xero_secret = settings.XERO_SECRET
    xero_callback = settings.XERO_CALLBACK

    credentials = OAuth2Credentials(
        client_id, xero_secret, callback_uri=xero_callback,
        scope=[
            XeroScopes.OFFLINE_ACCESS,
            XeroScopes.ACCOUNTING_CONTACTS,
            XeroScopes.ACCOUNTING_TRANSACTIONS
        ]
    )
    authorization_url = credentials.generate_url()
    caches['default'].set('xero_creds', credentials.state)
    return HttpResponseRedirect(authorization_url)


@staff_member_required
def xero_callback(request):
    cred_state = caches['default'].get('xero_creds')
    credentials = OAuth2Credentials(**cred_state)
    auth_secret = request.get_raw_uri()
    credentials.verify(auth_secret)
    credentials.set_default_tenant()
    caches['default'].set('xero_creds', credentials.state)
    return HttpResponseRedirect(reverse('xero_contacts'))


@staff_member_required
def xero_contacts(request):
    cred_state = caches['default'].get('xero_creds')
    if not cred_state:
        return HttpResponseRedirect(reverse('xero_auth'))

    credentials = OAuth2Credentials(**cred_state)
    if credentials.expired():
        credentials.refresh()
        caches['default'].set('xero_creds', credentials.state)
    xero_api = Xero(credentials)
    print(f"xero_api: {xero_api}")
    contacts = xero_api.contacts.all()
    print(f"contacts: {contacts}")
    context = {
        'contacts': contacts
    }
    return render(request, 'wilma/xero_contacts.html', context)
