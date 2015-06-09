from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Movie(models.Model):
    movieid = models.IntegerField()
    title = models.CharField(max_length=100)
    genres = models.CharField(max_length=150)

    def average_rating(self):
        return '1'

    def __str__(self):
        return "{}: {}".format(self.movieid, self.title)

class Rater(models.Model):
    userid = models.IntegerField()
    age = models.IntegerField()
    gender = models.CharField(max_length=1)
    occupation = models.IntegerField()
    zipcode = models.IntegerField()

    def average_mov_rating(self):
        return '1'

    def __str__(self):
        return "{}".format(self.userid)

class Rating(models.Model):
    userid = models.ForeignKey(Rater)
    movieid = models.ForeignKey(Movie)
    rating = models.IntegerField()
    timestamp = models.IntegerField