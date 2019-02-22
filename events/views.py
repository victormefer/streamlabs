from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import requests

from .utils import Utils


def events(request):
    streamer = request.POST.get('favorite')
    token = request.POST.get('token')

    # get streamer user info
    user = Utils.get_user_data(streamer, token)
    # subscribe to user follower events
    Utils.subscribe_user_followers(user['id'], token)

    context = {'streamer': streamer}
    return render(request, 'events/events.html', context=context)


@csrf_exempt
def get_followers(request):
    if request.method == 'GET':
        mode = request.GET.get('hub.mode')
        if mode:
            if mode == 'subscribe':
                challenge = request.GET.get('hub.challenge')
                print('FUNFOU!!!')
                return HttpResponse(content=challenge)
            elif mode == 'unsubscribe':
                challenge = request.GET.get('hub.challenge')
                print('Unsubscribed from event')
                return HttpResponse(content=challenge)
            elif mode == 'denial':
                print('Event subscription denied!')
                return HttpResponse()
    else:
        print("HELLLOU!!!!!")
        # print(request.body)
        # import pdb;pdb.set_trace()
        return HttpResponse()
