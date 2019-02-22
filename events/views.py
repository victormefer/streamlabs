from django.shortcuts import render

import requests


def events(request):
    streamer = request.POST.get('favorite')
    token = request.POST.get('token')

    # get streamer user info
    params = {'login': streamer}
    headers = {'Authorization': 'Bearer %s' % token}
    user_req = requests.get('https://api.twitch.tv/helix/users', params=params,
                            headers=headers)
    user = user_req.json()['data'][0]

    data = {
        'callback': '',
        'mode': 'subscribe',
        'lease_seconds': '864000',
        'topic': 'https://api.twitch.tv/helix/users/follows?first=1&to_id={}'
                 .format(user['id'])
    }
    req = requests.post('https://api.twitch.tv/helix/webhooks/hub', data=data)

    context = {'streamer': streamer}
    return render(request, 'events/events.html', context=context)


# def verify_subscription


# def get_user_follows(request):
#     request.
