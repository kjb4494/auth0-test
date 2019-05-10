from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as log_out
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from urllib.parse import urlencode
import requests
import json
from pprint import pprint as prt


# Create your views here.
def index(request):
    return render(request, 'index.html')


@login_required
def dashboard(request):
    user = request.user
    auth0user = user.social_auth.get(provider='auth0')
    userdata = {
        'user_id': auth0user.uid,
        'name': user.first_name,
        'picture': auth0user.extra_data['picture']
    }

    return render(request, 'dashboard.html', {
        'auth0User': auth0user,
        'userdata': json.dumps(userdata, indent=4)
    })


def logout(request):
    log_out(request)
    return_to = urlencode({'returnTo': request.build_absolute_uri('/')})
    logout_url = 'https://%s/v2/logout?client_id=%s&%s' % \
                 (settings.SOCIAL_AUTH_AUTH0_DOMAIN, settings.SOCIAL_AUTH_AUTH0_KEY, return_to)
    return HttpResponseRedirect(logout_url)


def api_test(request):
    return render(request, 'api_test.html')


def token(request):
    user = request.user
    auth0user = user.social_auth.get(provider='auth0')
    print(auth0user.uid)
    code = request.GET.get('code')
    url = 'https://' + settings.SOCIAL_AUTH_AUTH0_DOMAIN + '/oauth/token'
    header = {'content-type': "application/x-www-form-urlencoded"}
    payload = {
        'grant_type': 'authorization_code',
        'client_id': settings.SOCIAL_AUTH_AUTH0_KEY,
        'client_secret': settings.SOCIAL_AUTH_AUTH0_SECRET,
        'code': code,
        'redirect_uri': 'http://localhost:3000/token'
    }

    res = requests.post(url=url, data=payload, headers=header)
    result = ''
    res_dict = res.json()
    for value in res_dict:
        result += value + ': ' + str(res_dict[value]) + '<br>'
    result += '<p>---API Message---<br>'
    if res_dict.get('access_token') is not None:
        res = requests.get(
            url='http://localhost:3010/api/private',
            headers={
                'authorization': 'Bearer ' + res_dict.get('access_token')
            }
        )
        for value in res.json():
            result += res.json()[value]
    return HttpResponse(result)
