from django.shortcuts import render
from django.db.models import Count, Avg
from django.shortcuts import render
from .models import Movie, Rater, Rating

# Create your views here.

def top_movies(request):
    avg_movs = Rating.ratings.values("movieid").annotate(average_rating=Avg('rating'))
    top_movs = avg_movs.order_by("-average_rating")[0:20]
    mov_obs = [Movie.movies.get(pk=mov["movieid"]) for mov in top_movs]
    zipped = zip(top_movs, mov_obs)
    return render(request,
                  "ratings/topmovies.html",
                  {"movs": zipped})


def show_user(request, user_id):
    user = Rater.raters.get(pk=user_id)
    ratings = Rating.ratings.filter(userid=user_id)
    movs = []
    for rating in ratings:
        movs.append(rating.movieid)
    rates = []
    for rate in ratings:
        rates.append(rate.rating)
    average = sum(rates) / len(rates)
    zipped = zip(rates, movs)
    return render(request,
                  "ratings/show_user.html",
                  {"user": user,
                   "average": average,
                   "gender": user.gender,
                   "age": user.age,
                   "zipcode": user.zipcode,
                   "ratings": zipped})

def show_movie(request, movie_id):
    movie = Movie.movies.get(pk=movie_id)
    ratings = Rating.ratings.filter(movieid=movie_id)
    users = []
    for rating in ratings:
        users.append(rating.userid)
    rates = []
    for rate in ratings:
        rates.append(rate.rating)
    average = sum(rates) / len(rates)
    zipped = zip(rates, users)
    return render(request,
                  "ratings/show_movie.html",
                  {"movie": movie,
                   "average": average,
                   "ratings": zipped})