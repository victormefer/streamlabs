# Twitch Favorite Streamer

App for view the livestream and user events for your favorite Twitch streamer

## Live demo

See the live demo [here](https://twitch-favorite-streamer.herokuapp.com)

## Development

This app was developed with Python and Django, using the Django templates to easily and quicky implement the front-end pages. No database/models were used, since there was no specification of data to be saved. The app simply uses the Twitch API to log in the user, connects via Webhooks to get events for a given user/channel and shows a livestream, chat and the most recents events for that user/channel.

The events acquired are user follow events (the given user being followed by or starting to follow another user) and stream state changes, which are the ones available in the new Twitch API.

The app uses Websockets to show the events in real-time in the web page, using an ASGI server with Django Channels and Redis.

There are many details to still be polished in this app. The API tokens are not refreshed unless the first page is reloaded, leading to an error when the token has expired. The webhook connection is always made, even if one connection is still valid, and when returning to the first page and entering another streamer's name, events for the old streamer will still be shown in the stream page, along with events for the new streamer. These errors were not fixed because of time constraints - priority was given to getting the required features working in a basic form. There are also optimizations to be done, like acquiring the user token and user id, which can be done with a single request. However, limited knowledge of the Twitch API lead to this being implemented with multiple request in succession. The user access token is also propagated through the app in the requests data, but it could be passed via headers or cookies.

Finally, Heroku was used to deploy the live demo for its ease of use and free pricing.

In conclusion, the app was succesfully built and deployed in a basic working condition. There are still errors to be fixed and details to be improved upon, but given time constraints and limited knowledge of the API they were not prioritized.

## Deployment in AWS

Ideally, the app should be split into multiple availability zones for increased availability. Since it doesn't access a database storage, we just need to have EC2 instances running inside subnets in each availability zone, and a elastic load balancer to balance requests for each zone. The user accesses the client app, which connects via websockets to the back-end to consume events. With Amazon Auto Scaling we could make sure that there are enough instances running to handle all user accesses. Eventually, more availability zones might be required to increase available as the number of daily request grows.