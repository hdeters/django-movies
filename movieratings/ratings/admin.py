from django.contrib import admin
from .models import Movie, Rating, Rater

class MovieAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'average_rating', 'top_movies']

class RatingsAdmin(admin.ModelAdmin):
    list_display = ['movieid', 'userid', 'rating']

class RaterAdmin(admin.ModelAdmin):
    list_display = ['id', 'age', 'gender', 'average_movie_rating', 'top_movies_you_havent_seen']

# Register your models here.

admin.site.register(Movie, MovieAdmin)
admin.site.register(Rating, RatingsAdmin)
admin.site.register(Rater, RaterAdmin)