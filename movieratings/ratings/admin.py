from django.contrib import admin
from .models import Movie, Rating, Rater

class MovieAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']

class RatingsAdmin(admin.ModelAdmin):
    list_display = ['movieid', 'userid', 'rating']

class RaterAdmin(admin.ModelAdmin):
    list_display = ['id', 'age', 'gender']

# Register your models here.

admin.site.register(Movie, MovieAdmin)
admin.site.register(Rating, RatingsAdmin)
admin.site.register(Rater, RaterAdmin)