from django.shortcuts import render

import requests


def events(request):
    streamer = request.POST.get('favorite')

    # get streamer user id
    req = requests.get('https//api.twitch.tv/helix/users', {
        'login': streamer
    })

    # get user id from request

    data = {
        'callback': '',
        'mode': 'subscribe',
        'topic': ''
    }
    req = requests.post('https://api.twitch.tv/helix/webhooks/hub',
        'https://api.twitch.tv/helix/users/follows?first=1&from_id={}'.format(user.id))

    context = {'streamer': streamer}
    return render(request, 'events/events.html', context=context)
