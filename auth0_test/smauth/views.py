from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as log_out
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from urllib.parse import urlencode
from .models import Token
from datetime import datetime, timedelta
import requests
import json
import pytz
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
    try:
        user = request.user.social_auth.get(provider='auth0')
    except Exception as e:
        return HttpResponse('social_auth Error: ' + str(e))
    tk = Token.objects.filter(uid=user.uid)
    if not tk.exists():
        # Get Access Token
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
        access_token_data = res.json()
        access_token = access_token_data.get('access_token')
        expires = datetime.now(tz=pytz.UTC) + timedelta(seconds=access_token_data.get('expires_in'))
        token_type = access_token_data.get('token_type')
        tk = Token(
            uid=user.uid,
            access_token=access_token,
            expires=expires,
            token_type=token_type
        )
        tk.save()
        display_result = 'Access Token is created!<br>'
    else:
        access_token = tk[0].access_token
        expires = tk[0].expires
        token_type = tk[0].token_type
        display_result = 'You already exist access token!<br>'

    display_result += '-' * 60 + '<br>' + \
                      'access_token: ' + access_token + '<br>' + \
                      'expires: ' + str(expires) + '<br>' + \
                      'token_type: ' + token_type + '<br>' + \
                      '-' * 60 + '<p>'
    # API Test
    if access_token is not None:
        display_result += '--- API Message ---<br>'
        res = requests.get(
            url='http://localhost:3010/api/private',
            headers={
                'authorization': 'Bearer ' + access_token
            }
        )
        for key, value in res.json().items():
            display_result += key + ': ' + value + '<br>'
    return HttpResponse(display_result)
