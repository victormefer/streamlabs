from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from asgiref.sync import async_to_sync
import channels.layers

import requests
import json

from .utils import Utils


def events(request):
    streamer = request.POST.get('favorite')
    token = request.POST.get('token')

    # get streamer user info
    user = Utils.get_user_data(streamer, token)

    # subscribe to user events
    Utils.subscribe_user_followers(user['id'], token)
    Utils.subscribe_user_following(user['id'], token)
    Utils.subscribe_stream_changed(user['id'], token)

    context = {'streamer': streamer}
    return render(request, 'events/events.html', context=context)


@csrf_exempt
def get_followers(request):
    if request.method == 'GET':
        mode = request.GET.get('hub.mode')
        if mode:
            if mode == 'subscribe':
                challenge = request.GET.get('hub.challenge')
                print('===== Subscription successful!')
                return HttpResponse(content=challenge)
            elif mode == 'unsubscribe':
                challenge = request.GET.get('hub.challenge')
                print('===== Unsubscribed from event')
                return HttpResponse(content=challenge)
            elif mode == 'denial':
                print('===== ERROR - Event subscription denied! ====')
                return HttpResponse()
    else:
        print("===== Event received =====")
        data = json.loads(request.body)
        print(data)
        user = data['data'][0]['to_name']
        follower = data['data'][0]['from_name']
        message = 'User {} has started following {}'.format(follower, user)

        try:
            channel_layer = channels.layers.get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'event-consumer',
                {
                    'type': 'send_message',
                    'text': message
                }
            )
        except ConnectionRefusedError as ex:
            print('===== ERROR on sending message via websocket =====')
            print(ex)

        return HttpResponse() # tell twitch server the event was received


@csrf_exempt
def get_following(request):
    if request.method == 'GET':
        mode = request.GET.get('hub.mode')
        if mode:
            if mode == 'subscribe':
                challenge = request.GET.get('hub.challenge')
                print('===== Subscription successful!')
                return HttpResponse(content=challenge)
            elif mode == 'unsubscribe':
                challenge = request.GET.get('hub.challenge')
                print('===== Unsubscribed from event')
                return HttpResponse(content=challenge)
            elif mode == 'denial':
                print('===== ERROR - Event subscription denied! ====')
                return HttpResponse()
    else:
        print("===== Event received =====")
        data = json.loads(request.body)
        print(data)
        following = data['data'][0]['to_name']
        user = data['data'][0]['from_name']
        message = '{} has started following the user {}'.format(user, following)

        try:
            channel_layer = channels.layers.get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'event-consumer',
                {
                    'type': 'send_message',
                    'text': message
                }
            )
        except ConnectionRefusedError as ex:
            print('===== ERROR on sending message via websocket =====')
            print(ex)

        return HttpResponse() # tell twitch server the event was received


@csrf_exempt
def get_stream_changed(request):
    if request.method == 'GET':
        mode = request.GET.get('hub.mode')
        if mode:
            if mode == 'subscribe':
                challenge = request.GET.get('hub.challenge')
                print('===== Subscription successful!')
                return HttpResponse(content=challenge)
            elif mode == 'unsubscribe':
                challenge = request.GET.get('hub.challenge')
                print('===== Unsubscribed from event')
                return HttpResponse(content=challenge)
            elif mode == 'denial':
                print('===== ERROR - Event subscription denied! ====')
                return HttpResponse()
    else:
        print("===== Event received =====")
        response = json.loads(request.body)
        data = response['data']
        if not data or data == {}:
            message = 'Channel is now offline'
        else:
            message = 'Channel {} is now online'.format(data[0]['user_name'])

        try:
            channel_layer = channels.layers.get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'event-consumer',
                {
                    'type': 'send_message',
                    'text': message
                }
            )
        except ConnectionRefusedError as ex:
            print('===== ERROR on sending message via websocket =====')
            print(ex)

        return HttpResponse() # tell twitch server the event was received
