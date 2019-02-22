from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings

import requests


def login(request):
    code = request.GET.get('code')
    if code:
        data = {
            'client_id': settings.TWITCH_CLIENT_ID,
            'client_secret': settings.TWITCH_CLIENT_SECRET,
            'redirect_uri': 'http://localhost:8000',
            'code': code,
            'grant_type': 'authorization_code',
        }
        token_request = requests.post('https://id.twitch.tv/oauth2/token', data=data)
        response = token_request.json()

        return render(request, 'login/login.html', context=response)
    # import pdb;pdb.set_trace()
    # token = request.GET.get('access_token')
    # if token:
    #     context = {'token': token}
    #     return render(request, 'login/login.html', context=context)
    else:
        params = {
            'client_id': settings.TWITCH_CLIENT_ID,
            'redirect_uri': 'http://localhost:8000',
            'scope': 'channel:read:subscriptions'
        }
        return HttpResponseRedirect(
            'https://id.twitch.tv/oauth2/authorize'
            '?response_type=code&client_id={client_id}&'
            'redirect_uri={redirect_uri}&scope={scope}'.format(**params))
