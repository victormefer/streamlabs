from django.urls import path

from . import views


urlpatterns = [
    path('', views.events, name='events'),
    path('subs/user/followers', views.get_followers, name='user_followers'),
]
