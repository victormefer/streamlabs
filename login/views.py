from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings


def login(request):
    token = request.GET.get('code')
    if token:
        context = {'token': token}
        return render(request, 'login/login.html', context=context)
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
