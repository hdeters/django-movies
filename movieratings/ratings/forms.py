from django import forms
from django.contrib.auth.models import User
from ratings.models import Rater, Rating


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Rater
        fields = ('age', 'gender', 'zipcode',)

class NewRatingForm(forms.ModelForm):
    rating = forms.ChoiceField(choices=((1,1), (2,2), (3,3), (4,4), (5,5)))
    review = forms.Textarea()

    class Meta:
        model = Rating
        fields = ('movieid', 'rating', 'review')
