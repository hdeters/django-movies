from django.contrib.auth.models import User
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
    user = models.OneToOneField(User, null=True)
    raters = models.Manager()

    def __str__(self):
        return "{}".format(self.id)


class Rating(models.Model):
    userid = models.ForeignKey(Rater)
    movieid = models.ForeignKey(Movie)
    rating = models.IntegerField()
    ratings = models.Manager()


def create_users():
    for rater in Rater.raters.all():
        user = User.objects.create_user(username = '{}'.format(rater.id), email = '{}@emailaddress.net'.format(rater.id), password = 'password')
        rater.user = user
        rater.save()