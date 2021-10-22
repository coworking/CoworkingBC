from xero import Xero
from xero.auth import OAuth2Credentials
from xero.constants import XeroScopes

from django.conf import settings
from django.core.cache import caches
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect


def start_xero_auth(request):
    client_id = settings.XERO_CLIENT_ID
    client_secret = settings.XERO_SECRET
    callback_uri = settings.XERO_CALLBACK

    credentials = OAuth2Credentials(
        client_id, client_secret, callback_uri=callback_uri,
        scope=[
            XeroScopes.OFFLINE_ACCESS,
            XeroScopes.ACCOUNTING_CONTACTS,
            XeroScopes.ACCOUNTING_TRANSACTIONS
        ]
    )
    authorization_url = credentials.generate_url()
    caches['default'].set('xero_creds', credentials.state)
    return HttpResponseRedirect(authorization_url)


def process_callback(request):
    cred_state = caches['default'].get('xero_creds')
    credentials = OAuth2Credentials(**cred_state)
    auth_secret = request.get_raw_uri()
    credentials.verify(auth_secret)
    credentials.set_default_tenant()
    caches['default'].set('xero_creds', credentials.state)
    return HttpResponse("OK!")


def test_xero_auth(request):
    cred_state = caches['default'].get('xero_creds')
    credentials = OAuth2Credentials(**cred_state)
    if credentials.expired():
        credentials.refresh()
        caches['default'].set('xero_creds', credentials.state)
    xero = Xero(credentials)
    contacts = xero.contacts.all()
    json_response = "{'contacts': {0})}".format(len(contacts))
    return JsonResponse(json_response)
