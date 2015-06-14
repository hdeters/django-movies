from django.db.models import Count, Avg
from django.shortcuts import render, redirect
from .models import Movie, Rater, Rating
from django.contrib.auth import authenticate, login, logout
from ratings.forms import UserForm, ProfileForm, NewRatingForm
from django.contrib import messages

# Create your views here.

def index(request):
    """top_movies=Movie.objects.annotate(rating_count=Count('rating'),
                                        avg_rating=Avg('rating__rating'),
                                        ).filter(rating_count__gte=10).order_by('avg_rating)[:10]
    return render(request, 'ratings/index.html', {"top_movies: top_movies})"""
    avg_movs = Rating.ratings.values("movieid").annotate(average_rating=Avg('rating')).order_by("-average_rating")
    top = [mov for mov in avg_movs if Rating.ratings.filter(movieid=mov['movieid']).count() > 7]
    mov_obs = [Movie.movies.get(pk=mov["movieid"]) for mov in top][0:20]
    if request.user.is_authenticated():
        current_user = request.user.rater
        seen = [Rating.ratings.filter(movieid=mov.id, userid=current_user).exists() for mov in mov_obs]
        zipped = zip(top, mov_obs, seen)
        return render(request,
                    "ratings/index.html",
                    {"movs": zipped})
    else:
        zipped = zip(top, mov_obs)
        return render(request,
                  "ratings/index.html",
                  {"movs": zipped})



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
    average = sum(rates) / len(rates)
    zipped = zip(rates, movs)
    return render(request,
                  "ratings/show_user.html",
                  {"user": user,
                   "average": average,
                   "gender": user.gender,
                   "age": user.age,
                   "zipcode": user.zipcode,
                   "ratings": zipped,
                   "username": usrname})

def show_movie(request, movie_id):
    show_rate_movie = True
    movie = Movie.movies.get(pk=movie_id)
    ratings = Rating.ratings.filter(movieid=movie_id)
    users = []
    rates = []
    user_rating = 0
    for rating in ratings:
        users.append(rating.userid)
        rates.append(rating.rating)

    average = sum(rates) / len(rates)
    zipped = zip(rates, users)
    current_user = request.user.rater
    if request.user.is_authenticated():
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
                   "user_rating": user_rating})

def rate_movie(request, movie_id):
    if request.user.is_authenticated():
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
                    new_rate.save()
                    messages.add_message(
                    request,
                    messages.SUCCESS,
                    "Movie Successfully Rated.")
                return redirect('/movie/{}'.format(movie_id))
    else:
        return redirect('login')


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
            # The form doesn't know to call this special method on user.
            user.set_password(password)
            user.save()

            # You must call authenticate before login. :(
            user = authenticate(username=user.username,
                                password=password)
            login(request, user)
            messages.add_message(
                request,
                messages.SUCCESS,
                "Account Successfully Created.")
            return redirect('index')
    return render(request, "ratings/register.html", {'user_form': user_form,
                                                   'profile_form': profile_form})
