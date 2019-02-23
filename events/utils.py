import requests


class Utils():

    @staticmethod
    def get_user_data(user_login, token):
        params = {'login': user_login}
        headers = {'Authorization': 'Bearer %s' % token}
        user_resp = requests.get('https://api.twitch.tv/helix/users',
                                 params=params,
                                 headers=headers)
        user = user_resp.json()['data'][0]
        return user

    @staticmethod
    def subscribe_user_followers(user_id, token):
        headers = {'Authorization': 'Bearer %s' % token}
        data = {
            'hub.callback': 'http://4e412737.ngrok.io/'
                            'events/subs/user/followers',
            'hub.mode': 'subscribe',
            'hub.lease_seconds': '864000',
            'hub.topic':
                'https://api.twitch.tv/helix/users/follows?first=1&to_id={}'
                .format(user_id),
        }
        resp = requests.post('https://api.twitch.tv/helix/webhooks/hub',
                             data=data,
                             headers=headers)
        if resp.status_code != 202:
            import pdb;pdb.set_trace()
            print('Error on subscription request')

    @staticmethod
    def unsubscribe_user_followers(user_id, token):
        headers = {'Authorization': 'Bearer %s' % token}
        data = {
            'hub.callback': 'http://4e412737.ngrok.io/'
                            'events/subs/user/followers',
            'hub.mode': 'unsubscribe',
            'hub.topic':
                'https://api.twitch.tv/helix/users/follows?first=1&to_id={}'
                .format(user_id),
        }
        resp = requests.post('https://api.twitch.tv/helix/webhooks/hub',
                             data=data,
                             headers=headers)
        if resp.status_code != 202:
            print('Error on subscription request')
