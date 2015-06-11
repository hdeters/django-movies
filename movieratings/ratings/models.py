from django.db import models

# Create your models here.

class Movie(models.Model):
    title = models.CharField(max_length=255)
    movies = models.Manager()

    def __str__(self):
        return "{}: {}".format(self.id, self.title)
    

class Rater(models.Model):
    age = models.IntegerField()
    gender = models.CharField(max_length=1)
    zipcode = models.CharField(max_length=10)
    raters = models.Manager()

    def __str__(self):
        return "{}".format(self.id)


class Rating(models.Model):
    userid = models.ForeignKey(Rater)
    movieid = models.ForeignKey(Movie)
    rating = models.IntegerField()
    ratings = models.Manager()