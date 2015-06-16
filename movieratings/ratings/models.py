from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError


# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length=255)


class Movie(models.Model):
    title = models.CharField(max_length=255)
    #raters = models.ManyToManyField(Rater, through="Rating")
    genre = models.ManyToManyField(Genre)
    movies = models.Manager()

    def __str__(self):
        return "{}: {}".format(self.id, self.title)

    @property
    def get_genres(self):
        return [the_genre.name for the_genre in self.genre.all()]


class Rater(models.Model):
    age = models.IntegerField()
    gender = models.CharField(max_length=1)
    zipcode = models.CharField(max_length=10)
    user = models.OneToOneField(User, null=True)
    raters = models.Manager()

    def __str__(self):
        return "{}".format(self.id)

def validate_rating(value):
        if 0 < value < 6:
            pass
        else:
            raise ValidationError('{} is not a valid rating'.format(value))

class Rating(models.Model):
    userid = models.ForeignKey(Rater)
    movieid = models.ForeignKey(Movie)
    rating = models.IntegerField(validators=[validate_rating])
    date = models.DateTimeField(default=timezone.now)
    review = models.TextField(null=True, blank=True)
    ratings = models.Manager()


def create_users():
    for rater in Rater.raters.all():
        user = User.objects.create_user(username='{}'.format(rater.id), email='{}@emailaddress.net'.format(rater.id), password='password')
        rater.user = user
        rater.save()


