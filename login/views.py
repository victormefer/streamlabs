from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings

import requests


# Create your views here.
def login(request):
    if (request.method == 'POST'):
        # log in user
        params = {
            'client_id': settings.TWITCH_CLIENT_ID,
            'redirect_uri': 'http://localhost:8000',
            'response_type': 'token',
            'scope': 'channel:read:subscriptions'
        }
        req = requests.get('https://id.twitch.tv/oauth2/authorize',
                           params=params)
        import pdb;pdb.set_trace()
        return HttpResponse(req.text)

    return render(request, 'login/login.html')
