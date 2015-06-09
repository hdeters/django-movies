from django.db import models

# Create your models here.

class Movie(models.Model):
    title = models.CharField(max_length=100)
    genres = models.CharField(max_length=150)
    movies = models.Manager()

    @property
    def average_rating(self):
        total = 0
        for rating in Rating.ratings.filter(movieid = self.id):
            total = total + rating.rating
        return total / len(Rating.ratings.filter(movieid = self.id))

    @classmethod
    def top_movies(cls):
        all_movs =  Movie.movies.all()
        sorted_movs = sorted(all_movs, key=lambda x: x.average_rating, reverse=True)
        return sorted_movs[0:10]

    def __str__(self):
        return "{}: {}".format(self.id, self.title)

class Rater(models.Model):
    age = models.IntegerField()
    gender = models.CharField(max_length=1)
    occupation = models.IntegerField()
    zipcode = models.IntegerField()
    raters = models.Manager()

    @property
    def average_movie_rating(self):
        total = 0
        if len(Rating.ratings.filter(userid = self.id)) == 0:
            return 0
        else:
            for rating in Rating.ratings.filter(userid = self.id):
                total = total + rating.rating
            return total / len(Rating.ratings.filter(userid = self.id))

    @property
    def top_movies_you_havent_seen(self):
        if len(Rating.ratings.filter(userid = self.id)) == 0:
            return 0
        else:
            movs_seen =  [rating.movieid for rating in Rating.ratings.filter(userid = self.id)]
            all_movs = Movie.movies.all()
            top_movs = []
            for mov in all_movs:
                if mov not in movs_seen:
                    top_movs.append(mov)
            sorted_movs = sorted(top_movs, key=lambda x: x.average_rating, reverse=True)
            return sorted_movs[0:10]

    def __str__(self):
        return "{}".format(self.id)

class Rating(models.Model):
    userid = models.ForeignKey(Rater)
    movieid = models.ForeignKey(Movie)
    rating = models.IntegerField()
    timestamp = models.IntegerField
    ratings = models.Manager()