from django.urls import path

from . import views


urlpatterns = [
    path('', views.events, name='events'),
    path('subs/user/followers', views.get_followers, name='user_followers'),
    path('subs/user/following', views.get_following, name='user_following'),
    path('subs/stream', views.get_stream_changed, name='stream_changed'),
]
