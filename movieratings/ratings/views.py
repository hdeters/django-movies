from django.contrib.auth.models import User
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Count, Avg
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, View, UpdateView, DeleteView
from .models import Movie, Rater, Rating, Genre
from django.contrib.auth import authenticate, login
from ratings.forms import UserForm, ProfileForm, NewRatingForm
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# class LoginRequiredMixin(object):
#     @method_decorator(login_required)
#     def dispatch(self, request, *args, **kwargs):
#         return super().dispatch(request, *args, **kwargs)

class MovieListView(ListView):
    model = Movie
    context_object_name = 'top_movies'
    queryset = Movie.movies.annotate(rating_count=Count('rating'),
                                     avg_rating=Avg('rating__rating'), ).filter(rating_count__gte=10).order_by(
        '-avg_rating')
    paginate_by = 20
    template_name = 'ratings/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header"] = "Top Movies"
        if self.request.user.is_authenticated():
            current_user = self.request.user.rater
            user_ratings = Rating.ratings.filter(userid=current_user).values_list('movieid', flat=True)
        else:
            user_ratings = []
        context["user_ratings"] = user_ratings
        return context


def show_genres(request):
    genres = Genre.objects.all()
    return render(request, 'ratings/show_genres.html', {"genres": genres})


class GenreListView(ListView):
    model = Movie
    context_object_name = 'top_genre'
    paginate_by = 20
    template_name = 'ratings/genre_list.html'

    def get_queryset(self):
        the_genre = Genre.objects.get(pk=self.kwargs['genre_id'])
        return Movie.movies.annotate(rating_count=Count('rating'),
                                         avg_rating=Avg('rating__rating'), ).filter(rating_count__gte=7,
                                                                                    genre=the_genre).order_by(
            '-avg_rating')

    def get_context_data(self, **kwargs):
        the_genre = Genre.objects.get(pk=self.kwargs['genre_id'])
        context = super().get_context_data(**kwargs)
        context["header"] = the_genre.name
        if self.request.user.is_authenticated():
            current_user = self.request.user.rater
            user_ratings = Rating.ratings.filter(userid=current_user).values_list('movieid', flat=True)
        else:
            user_ratings = []
        context["user_ratings"] = user_ratings
        return context


class RateFreqListView(ListView):
    model = Movie
    context_object_name = 'freq_movies'
    queryset = Movie.movies.annotate(rating_count=Count('rating'), ).order_by('-rating_count')
    paginate_by = 20
    template_name = 'ratings/rate_freq_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header"] = "Frequently Rated Movies"
        if self.request.user.is_authenticated():
            current_user = self.request.user.rater
            user_ratings = Rating.ratings.filter(userid=current_user).values_list('movieid', flat=True)
        else:
            user_ratings = []
        context["user_ratings"] = user_ratings
        return context


class ShowUserDetailView(DetailView):
    model = Rater
    context_object_name = 'user'
    paginate_by = 20
    template_name = 'ratings/show_user.html'

    def get_object(self, queryset=None):
        return Rater.raters.get(pk=self.kwargs['user_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ratings = Rating.ratings.filter(userid=self.kwargs['user_id']).select_related()
        movs = []
        for rating in ratings:
            movs.append(rating.movieid)
        zipped = zip(movs, ratings)
        context['ratings'] = zipped
        return context


class ShowRatingDetailView(DetailView):
    model = Rating
    context_object_name = 'rating'
    paginate_by = 20
    template_name = 'ratings/show_rating.html'

    def get_object(self, queryset=None):
        return Rating.ratings.get(pk=self.kwargs['rating_id'])

    def get_context_data(self, **kwargs):
        rating = Rating.ratings.get(pk=self.kwargs['rating_id'])
        movie = rating.movieid
        context = super().get_context_data(**kwargs)
        show_rate_movie = True
        if self.request.user.is_authenticated():
            if Rating.ratings.filter(movieid=movie.id, userid=self.request.user.rater.id).exists():
                show_rate_movie = False
                user_rating = Rating.ratings.filter(movieid=movie.id, userid=self.request.user.rater.id)[0]
            else:
                user_rating = 0
        else:
            show_rate_movie = True
            user_rating = None

        context['movie'] = movie
        context['rate'] = show_rate_movie
        context['user_rating'] = user_rating
        return context

class ShowMovieDetailView(DetailView):
    model = Movie
    context_object_name = 'movie'
    #paginate_by = 20
    template_name = 'ratings/show_movie.html'

    def get_object(self, queryset=None):
        return Movie.movies.get(pk=self.kwargs['movie_id'])

    def get_context_data(self, **kwargs):
        show_rate_movie = True
        user_rating = 0
        context = super().get_context_data(**kwargs)
        ratings = Rating.ratings.filter(movieid=self.kwargs['movie_id']).select_related()
        if len(ratings) > 20:
            paginate = True
        else:
            paginate = False
        if self.request.user.is_authenticated():
            current_user = self.request.user.rater
            if Rating.ratings.filter(movieid=self.kwargs['movie_id'], userid=current_user.id).exists():
                show_rate_movie = False
                user_rating = Rating.ratings.filter(movieid=self.kwargs['movie_id'], userid=current_user.id)[0]
        else:
            show_rate_movie = True
            user_rating = 0

        context['ratings'] = ratings
        context['rate'] = show_rate_movie
        context['user_rating'] = user_rating
        context['paginate'] = paginate
        return context



class RatingCreate(CreateView):
    model = Rating
    fields = ['movieid', 'rating', 'review']
    template_name = 'ratings/rate_movie.html'

    def form_valid(self, form):
        form.instance.userid = self.request.user.rater
        form.instance.date = timezone.now()
        messages.add_message(self.request, messages.SUCCESS,
                             "Your rating was successfully created!")
        return super().form_valid(form)


class AddRatingView(View):
    def get(self, request, **kwargs):
        form = NewRatingForm(initial={'movieid': Movie.movies.get(pk=self.kwargs['movie_id']), 'userid': self.request.user.rater})
        return render(request, "ratings/rate_movie.html", {"form": form})

    def post(self, request, **kwargs):
        form = NewRatingForm(request.POST, initial={'movieid': Movie.movies.get(pk=self.kwargs['movie_id']), 'userid': self.request.user.rater})
        if form.is_valid():
            rating = form.save(commit=False)
            rating.userid = request.user.rater
            rating.date = timezone.now()
            rating.save()
            messages.add_message(request, messages.SUCCESS,
                                 "Your rating was successfully created!")
            return redirect("index")
        else:
            return render(request, "ratings/rate_movie.html", {"form": form})


class RatingUpdate(UpdateView):
    model = Rating
    form_class = NewRatingForm
    template_name = 'ratings/rating_update_form.html'

    def get_success_url(self):
        return reverse('show_movie', kwargs={'movie_id': self.kwargs['movie_id']})

    def get_initial(self, **kwargs):
        return {'movieid': Movie.movies.get(pk=self.kwargs['movie_id']), 'userid': self.request.user.rater}

    def get_object(self, queryset=None, **kwargs):
        rating = Rating.ratings.filter(movieid=self.kwargs['movie_id']).get(userid=self.request.user.rater)
        return rating

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        messages.add_message(self.request, messages.SUCCESS,
                                 "Your rating was successfully updated!")
        return super(RatingUpdate, self).form_valid(form)


class AddUserView(View):
    def get(self, request):
        user_form = UserForm()
        profile_form = ProfileForm()
        return render(request, "ratings/register.html", {"form1": user_form, "form2": profile_form})

    def post(self, request):
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

            login(self.request, user)
            messages.add_message(
                request,
                messages.SUCCESS,
                "Account Successfully Created.")
            return redirect("index")
        else:
            return render(request, "ratings/rate_movie.html", {"form1": user_form, "form2": profile_form})


class RatingDelete(DeleteView):
    model = Rating
    success_url = reverse_lazy('index')

    def get_object(self, queryset=None):
        return Rating.ratings.filter(pk=self.kwargs['rate_id'])
