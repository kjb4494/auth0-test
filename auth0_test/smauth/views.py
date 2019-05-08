from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as log_out
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from urllib.parse import urlencode
import requests
import json


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


def token(response):
    code = response.GET.get('code')
    url = 'https://dev-d9lwdkbd.auth0.com/oauth/token'
    header = {'content-type': "application/x-www-form-urlencoded"}
    payload = {
        'grant_type': 'authorization_code',
        'client_id': '3OCfUZQsv5Xk9XnwbrB2lePmLjwEk7iC',
        'client_secret': 'RVHpLv5a-Mi5bJALEsCfr6MDRneVcvsd73erfECjtnuFAeHW2H9d0oPKi5KkZTyX',
        'code': code,
        'redirect_uri': 'http://localhost:3000/token'
    }

    res = requests.post(url=url, data=payload, headers=header)
    result = ''
    for value in res.json():
        result += value + ': ' + str(res.json()[value]) + '<br>'
    return HttpResponse(result)
