from django.db.models import Count, Avg
from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Rater, Rating, Genre
from django.contrib.auth import authenticate, login, logout
from ratings.forms import UserForm, ProfileForm, NewRatingForm
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    top_movies = Movie.movies.annotate(rating_count=Count('rating'),
                                        avg_rating=Avg('rating__rating'),).filter(rating_count__gte=10).order_by('-avg_rating')[:20]
    if request.user.is_authenticated():
        current_user = request.user.rater
        seen = [Rating.ratings.filter(movieid=mov.id, userid=current_user).exists() for mov in top_movies]
        zipped = zip(top_movies, seen)
        return render(request, 'ratings/index.html', {"top_movies": zipped})
    else:
        return render(request, 'ratings/index.html', {"top_movies": top_movies})


def show_user(request, user_id):
    user = Rater.raters.get(pk=user_id)
    usrname = user.user.get_username()
    ratings = Rating.ratings.filter(userid=user_id)
    movs = []
    for rating in ratings:
        movs.append(rating.movieid)
    rates = []
    for rate in ratings:
        rates.append(rate.rating)
    if len(rates) > 0:
        average = sum(rates) / len(rates)
    else:
        average = 0
    zipped = zip(rates, movs, ratings)
    return render(request,
                  "ratings/show_user.html",
                  {"user": user,
                   "average": average,
                   "gender": user.gender,
                   "age": user.age,
                   "zipcode": user.zipcode,
                   "ratings": zipped,
                   "username": usrname})

def show_rating(request, rating_id):
    show_rate_movie = True
    rating = get_object_or_404(Rating, pk=rating_id)
    movie = rating.movieid
    time = rating.date
    genres = movie.get_genres
    review = rating.review
    user = rating.userid.user.get_username()
    if request.user.is_authenticated():
        if Rating.ratings.filter(movieid=movie.id, userid=request.user.rater.id).exists():
            show_rate_movie = False
            user_rating = Rating.ratings.filter(movieid=movie.id, userid=request.user.rater.id)[0]
            usrname = request.user.get_username()
    else:
        show_rate_movie = True
        usrname = None
        user_rating = None

    return render(request,
                  "ratings/show_rating.html",
                  {"user": user,
                   "username": usrname,
                   "time": time,
                   "movie": movie,
                   "genres": genres,
                   "rating": rating,
                   "rate": show_rate_movie,
                   "user_rating": user_rating,
                   "review": review})

def show_movie(request, movie_id):
    show_rate_movie = True
    movie = Movie.movies.get(pk=movie_id)
    ratings = Rating.ratings.filter(movieid=movie_id)
    genres = movie.get_genres
    users = []
    rates = []
    user_rating = 0
    for rating in ratings:
        users.append(rating.userid)
        rates.append(rating.rating)

    average = sum(rates) / len(rates)
    zipped = zip(rates, users, ratings)

    if request.user.is_authenticated():
        current_user = request.user.rater
        if current_user in users:
            show_rate_movie = False
            for rating in ratings:
                if rating.userid == current_user:
                    user_rating = rating.rating
        else:
            show_rate_movie = True

    return render(request,
                  "ratings/show_movie.html",
                  {"movie": movie,
                   "average": average,
                   "ratings": zipped,
                   "rate": show_rate_movie,
                   "user_rating": user_rating,
                   "genres": genres,})

@login_required(login_url='/login/')
def rate_movie(request, movie_id):
    current_user_id = request.user.rater
    if Rating.ratings.filter(movieid=movie_id, userid=current_user_id).exists():
        old_rating = Rating.ratings.filter(movieid=movie_id).get(userid=current_user_id)
        if request.method == "GET":
            rate_form = NewRatingForm(initial={'movieid': Movie.movies.get(pk=movie_id), 'userid': current_user_id}, instance=old_rating)
            return render(request, "ratings/rate_movie.html", {'rate_form': rate_form, 'movie_var': movie_id,})
        elif request.method == "POST":
            rate_form = NewRatingForm(request.POST, initial={'movieid': Movie.movies.get(pk=movie_id), 'userid': current_user_id}, instance=old_rating)
            if rate_form.is_valid():
                rate_form.save()
                old_rating.save()
                messages.add_message(
                request,
                messages.SUCCESS,
                "Rating Successfully Changed.")
            return redirect('/movie/{}'.format(movie_id))
    else:
        if request.method == "GET":
            rate_form = NewRatingForm(initial={'movieid': Movie.movies.get(pk=movie_id), 'userid': current_user_id})
            return render(request, "ratings/rate_movie.html", {'rate_form': rate_form, 'movie_var': movie_id,})
        elif request.method == "POST":
            rate_form = NewRatingForm(request.POST, initial={'movieid': Movie.movies.get(pk=movie_id), 'userid': current_user_id})
            if rate_form.is_valid():
                new_rate = rate_form.save(commit=False)
                new_rate.userid = request.user.rater
                new_rate.date = timezone.now()
                new_rate.save()
                messages.add_message(
                request,
                messages.SUCCESS,
                "Movie Successfully Rated.")
            return redirect('/movie/{}'.format(movie_id))


def user_register(request):
    if request.method == "GET":
        user_form = UserForm()
        profile_form = ProfileForm()
    elif request.method == "POST":
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            password = user.password
            user.set_password(password)
            user.save()

            user = authenticate(username=user.username,
                                password=password)
            login(request, user)
            messages.add_message(
                request,
                messages.SUCCESS,
                "Account Successfully Created.")
            return redirect('index')
    return render(request, "ratings/register.html", {'user_form': user_form, 'profile_form': profile_form})

@login_required
def delete_rating(request, rate_id):
    rating = Rating.ratings.get(pk=rate_id)
    rating.delete()
    messages.add_message(request, messages.SUCCESS,
                             "You have deleted this rating.")
    return redirect("show_user", request.user.rater.id)

def show_genres(request):
    genres = Genre.objects.all()
    return render(request, 'ratings/show_genres.html', {"genres": genres})

def show_genre(request, genre_id):
    the_genre = Genre.objects.get(pk=genre_id)
    top_movies = Movie.movies.annotate(rating_count=Count('rating'),
                                        avg_rating=Avg('rating__rating'),).filter(rating_count__gte=7).order_by('-avg_rating').filter(
                                        genre=the_genre)[0:20]
    if request.user.is_authenticated():
        current_user = request.user.rater
        seen = [Rating.ratings.filter(movieid=mov.id, userid=current_user).exists() for mov in top_movies]
        zipped = zip(top_movies, seen)
        return render(request, 'ratings/show_genre.html', {"top_movies": zipped, "genre": the_genre.name})
    else:
        return render(request, 'ratings/show_genre.html', {"top_movies": top_movies, "genre": the_genre.name})

def freq_rated(request):
    top_movies = Movie.movies.annotate(rating_count=Count('rating'),).order_by('-rating_count')[:20]
    if request.user.is_authenticated():
        current_user = request.user.rater
        seen = [Rating.ratings.filter(movieid=mov.id, userid=current_user).exists() for mov in top_movies]
        zipped = zip(top_movies, seen)
        return render(request, 'ratings/freq_rated.html', {"top_movies": zipped})
    else:
        return render(request, 'ratings/freq_rated.html', {"top_movies": top_movies})
