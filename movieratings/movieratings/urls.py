"""movieratings URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from ratings import views as ratings_views
from django.contrib.auth import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'index/', ratings_views.index, name="index"),
    url(r'^user/(?P<user_id>\d+)$', ratings_views.show_user, name="show_user"),
    url(r'^rating/(?P<rating_id>\d+)$', ratings_views.show_rating, name="show_rating"),
    url(r'^rate/(?P<movie_id>\d*)$', ratings_views.rate_movie, name="rate_movie"),
    url(r'^movie/(?P<movie_id>\d+)$', ratings_views.show_movie, name="show_movie"),
    url(r'^login/$', views.login, {'template_name': 'ratings/login.html'}, name="login"),
    url(r'^logout/$', views.logout, {'next_page': 'login'}, name='logout'),
    url(r'^delete/(?P<rate_id>\d+)$', ratings_views.delete_rating, name='delete_rating'),
    url(r'^register/$', ratings_views.user_register, name="user_register"),
    url(r'genre/(?P<genre_id>\d+)$', ratings_views.show_genre, name="show_genre"),
    url(r'genres/', ratings_views.show_genres, name="show_genres"),
    url(r'freq/', ratings_views.freq_rated, name="freq_rated"),
]
